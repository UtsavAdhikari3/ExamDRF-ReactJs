from django.db import models
from django.utils import timezone
from accounts.models import User

class Question(models.Model):
    """
    Model for storing exam questions with multiple choice options.
    """
    QUESTION_TYPES = (
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('descriptive', 'Descriptive'),
    )
    
    question = models.TextField()
    question_type = models.CharField(max_length=15, choices=QUESTION_TYPES, default='mcq')
    options = models.JSONField()  # Stores a list of options as JSON
    answer = models.IntegerField()  # Index of the correct answer (0-based)
    explanation = models.TextField(blank=True, null=True)  # Explanation for the answer
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_questions')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.question[:50]

class Exam(models.Model):
    """
    Model for storing exam information, including practice and live exams.
    """
    EXAM_TYPES = (
        ('practice', 'Practice Exam'),
        ('live', 'Live Exam'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPES, default='practice')
    is_live = models.BooleanField(default=False)  # False for practice exams, True for live exams
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 0 for practice exams
    scheduled_date = models.DateTimeField(null=True, blank=True)  # Only for live exams
    duration = models.IntegerField(default=30)  # Duration in minutes
    questions = models.ManyToManyField(Question, related_name='exams', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_exams')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_active(self):
        """
        Check if a live exam is currently active (within the scheduled time window).
        """
        if not self.is_live or not self.scheduled_date:
            return False
        
        now = timezone.now()
        end_time = self.scheduled_date + timezone.timedelta(minutes=self.duration)
        return self.scheduled_date <= now <= end_time

class Result(models.Model):
    """
    Model for storing exam results for both practice and live exams.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    score = models.IntegerField()
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)  # Percentage
    rank = models.IntegerField(null=True, blank=True)  # Rank among all participants
    incorrect_count = models.IntegerField(default=0)
    tab_switches = models.IntegerField(default=0)  # Number of tab switches during exam
    questions = models.ManyToManyField(Question, through='ResultQuestion')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.exam.title} - {self.score}"
    
    class Meta:
        indexes = [
            models.Index(fields=['exam']),
            models.Index(fields=['user']),
        ]

class ResultQuestion(models.Model):
    """
    Through model for storing which questions were included in a result and the user's answers.
    """
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.IntegerField(null=True, blank=True)  # Index of user's answer, null if unanswered
    is_correct = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('result', 'question')
    
    def __str__(self):
        return f"{self.result.user.username} - Q{self.question.id} - A{self.user_answer}"


class Leaderboard(models.Model):
    """
    Model for storing leaderboard information for exams.
    """
    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, related_name='leaderboard')
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Leaderboard - {self.exam.title}"
    
    def get_top_performers(self, limit=10):
        """
        Get the top performers for this exam.
        """
        return self.exam.results.order_by('-score', 'created_at')[:limit]
