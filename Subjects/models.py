"""  
This is the Subjects Model where we can define the subjects that we will be offering
"""
from django.db import models


class Subjects(models.Model):
    """  
    This is the Subjects Model
    """
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """  
        Meta class for Subjects Model
        """
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f'{self.name}'
