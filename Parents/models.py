"""
This is the Model for the Parent Database
"""

from django.db import models


class Parents (models.Model):
    """  This is the Parent Profiles Model """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True)
    stripe_id = models.CharField(
        max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """ Meta class for Parents Model """
        verbose_name = 'Parent'
        verbose_name_plural = 'Parents'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['phone']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
