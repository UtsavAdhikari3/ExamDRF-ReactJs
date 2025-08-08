from rest_framework import serializers
from accounts.models import User
from exam.models import Exam, Question, Result, ResultQuestion, Leaderboard

class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'role_display', 'is_admin', 'is_superadmin', 'wallet_balance', 'created_at']
        read_only_fields = ['wallet_balance', 'created_at', 'is_admin', 'is_superadmin']

class QuestionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question', 'question_type', 'options', 'created_by', 'created_by_username', 'created_at']
        # Exclude answer field for security

class QuestionDetailSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question', 'question_type', 'options', 'answer', 'explanation', 'created_by', 'created_by_username', 'created_at']

class ExamSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'exam_type', 'exam_type_display', 'is_live', 'price', 
                  'scheduled_date', 'duration', 'created_by', 'created_by_username', 'created_at', 'question_count']
    
    def get_question_count(self, obj):
        return obj.questions.count()

class ExamDetailSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'exam_type', 'exam_type_display', 'is_live', 'price', 
                  'scheduled_date', 'duration', 'created_by', 'created_by_username', 'created_at', 'questions']

class ResultQuestionSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question')
    options = serializers.JSONField(source='question.options')
    correct_answer = serializers.IntegerField(source='question.answer')
    explanation = serializers.CharField(source='question.explanation')
    
    class Meta:
        model = ResultQuestion
        fields = ['question_text', 'options', 'correct_answer', 'explanation', 'user_answer', 'is_correct']

class ResultSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title')
    user_username = serializers.CharField(source='user.username')
    questions = ResultQuestionSerializer(source='resultquestion_set', many=True, read_only=True)
    
    class Meta:
        model = Result
        fields = ['id', 'user_username', 'exam_title', 'score', 'accuracy', 'rank', 
                  'tab_switches', 'created_at', 'questions']

class LeaderboardSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title')
    top_performers = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'exam_title', 'top_performers', 'updated_at']
    
    def get_top_performers(self, obj):
        top_results = obj.get_top_performers()
        return [{
            'username': result.user.username,
            'score': result.score,
            'accuracy': result.accuracy,
            'rank': result.rank,
            'created_at': result.created_at
        } for result in top_results]

class TransactionSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username')
    exam_title = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = ['id', 'user_username', 'amount', 'transaction_type', 
                  'description', 'created_at', 'exam_title']
    
    def get_exam_title(self, obj):
        if obj.exam:
            return obj.exam.title
        return None


