from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from exam.models import Question, Exam

class Command(BaseCommand):
    help = 'Seed test data for accounts and exam'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🌱 Seeding test data...'))

        # === USERS ===
        student, _ = User.objects.get_or_create(username='student1', defaults={
            'email': 'student1@example.com',
            'role': 'user'
        })
        student.set_password('testpass123')
        student.save()

        teacher, _ = User.objects.get_or_create(username='teacher1', defaults={
            'email': 'teacher1@example.com',
            'role': 'teacher',
            'is_staff': True
        })
        teacher.set_password('teachpass123')
        teacher.save()

        admin, _ = User.objects.get_or_create(username='admin1', defaults={
            'email': 'admin1@example.com',
            'role': 'superadmin',
            'is_staff': True,
            'is_superuser': True
        })
        admin.set_password('adminpass123')
        admin.save()

        # === QUESTIONS ===
        q1 = Question.objects.filter(question="What is the capital of France?").first()
        if not q1:
            q1 = Question.objects.create(
                question="What is the capital of France?",
                question_type="mcq",
                options=["Berlin", "Madrid", "Paris", "Rome"],
                answer=2,
                explanation="Paris is the capital of France.",
                created_by=teacher
            )

        q2 = Question.objects.filter(question="The Earth is flat.").first()
        if not q2:
            q2 = Question.objects.create(
                question="The Earth is flat.",
                question_type="true_false",
                options=["True", "False"],
                answer=1,
                explanation="Scientific consensus confirms the Earth is round.",
                created_by=teacher
            )

        q3 = Question.objects.filter(question="Explain Newton's First Law.").first()
        if not q3:
            q3 = Question.objects.create(
                question="Explain Newton's First Law.",
                question_type="descriptive",
                options=[],
                answer=0,
                created_by=teacher
            )

        # === EXAMS ===
        practice_exam = Exam.objects.filter(title="Geography Practice Test").first()
        if not practice_exam:
            practice_exam = Exam.objects.create(
                title="Geography Practice Test",
                description="A basic practice test on world geography.",
                exam_type="practice",
                is_live=False,
                price=0.00,
                duration=15,
                created_by=teacher
            )
            practice_exam.questions.set([q1, q2])

        live_exam = Exam.objects.filter(title="Science Live Exam").first()
        if not live_exam:
            live_exam = Exam.objects.create(
                title="Science Live Exam",
                description="Live exam for basic science concepts.",
                exam_type="live",
                is_live=True,
                price=5.00,
                scheduled_date=timezone.now() + timedelta(minutes=1),
                duration=20,
                created_by=teacher
            )
            live_exam.questions.set([q2, q3])

        self.stdout.write(self.style.SUCCESS('✅ Done seeding test data!'))
