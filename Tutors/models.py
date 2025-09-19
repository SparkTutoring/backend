from django.db import models
from utils.choices import GENDER, GROUP


class Tutors(models.Model):
    """This is the Tutor Profiles Model"""

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER)
    degree = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    group = models.CharField(max_length=50, choices=GROUP)
    calendarId = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta class for Tutors Model"""
        verbose_name = 'Tutor'
        verbose_name_plural = 'Tutors'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['phone']),
            models.Index(fields=['group']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
