from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser to include additional fields
    needed for the PSC Exam Platform.
    """
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('teacher', 'Teacher'),  # New teacher role
        ('admin', 'Admin'),
        ('superadmin', 'Super Admin'),
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_admin = models.BooleanField(default=False)  # Kept for backward compatibility
    is_superadmin = models.BooleanField(default=False)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def save(self, *args, **kwargs):
        # Ensure role and boolean flags are in sync
        if self.is_superuser:
            self.role = 'superadmin'
            self.is_admin = True
            self.is_superadmin = True
        elif self.is_staff:
            if not self.role or self.role =='user':
                self.role = 'admin'
            self.is_admin = True
            self.is_superadmin = False
        else:
            self.role = 'user'
            self.is_admin = False
            self.is_superadmin = False
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username
