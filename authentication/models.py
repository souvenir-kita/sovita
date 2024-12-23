from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('buyer', 'Buyer'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    address = models.TextField(max_length=200)
    age = models.PositiveIntegerField(null=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.role}"