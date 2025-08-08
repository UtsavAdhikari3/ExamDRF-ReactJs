from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .permissions import IsTeacherOrReadOnly
from .models import Exam, Question, Result, Leaderboard,ResultQuestion
from .serializers import (
    ExamSerializer,
    ExamDetailSerializer,
    QuestionSerializer,
    QuestionDetailSerializer,
    ResultSerializer,
    LeaderboardSerializer
)
from django.db import transaction
from rest_framework import status

class ExamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exam.objects.all().order_by('-created_at')
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='submit')
    @transaction.atomic
    def submit_exam(self, request, pk=None):
        exam = self.get_object()
        user = request.user
        answers = request.data.get("answers", {})  # {question_id: user_answer}

        if exam.is_live:
            if not exam.is_active:
                return Response(
                    {"error": "This exam is not active right now."},
                    status=status.HTTP_403_FORBIDDEN
                )
        if not isinstance(answers, dict):
            return Response({"error": "Answers must be a dictionary of {question_id: answer_index}."}, status=400)

        # Prevent resubmission
        existing = Result.objects.filter(user=user, exam=exam).first()
        if existing:
            return Response({"error": "You have already submitted this exam."}, status=400)

        score = 0
        incorrect = 0
        result = Result.objects.create(user=user, exam=exam, score=0, accuracy=0.0)
        result_questions = []

        for question in exam.questions.all():
            user_ans = answers.get(str(question.id))
            is_correct = False

            if user_ans is not None and question.question_type != 'descriptive':
                is_correct = int(user_ans) == question.answer
                if is_correct:
                    score += 1
                else:
                    incorrect += 1

            result_questions.append(ResultQuestion(
                result=result,
                question=question,
                user_answer=user_ans,
                is_correct=is_correct
            ))

        ResultQuestion.objects.bulk_create(result_questions)
        total = exam.questions.count()
        result.score = score
        result.incorrect_count = incorrect
        result.accuracy = (score / total) * 100 if total > 0 else 0
        result.save()

        # Update ranks
        results = Result.objects.filter(exam=exam).order_by('-score', 'created_at')
        for i, res in enumerate(results, start=1):
            res.rank = i
            res.save()

        return Response(ResultSerializer(result).data, status=status.HTTP_201_CREATED)

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('-created_at')
    serializer_class = QuestionDetailSerializer
    permission_classes = [IsTeacherOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list']:
            return QuestionSerializer
        return QuestionDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Users can view their own results.
    """
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(user=self.request.user).order_by('-created_at')


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View leaderboard for exams.
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]
