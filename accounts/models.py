from django.db import models
from django.contrib.auth.models import AbstractUser

class Accounts(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('viewer', 'Viewer'),
    ]
    
    account_id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    
    def __str__(self):
        return f"{self.username} ({self.role})"