from django.db import models
from utils.choices import GENDER, YEAR, SCHOOL_TYPE
from Parents.models import Parents


class Students(models.Model):
    """
    This is the Student Profiles Model
    """
    user = models.ForeignKey(
        'auth.User',
        # or models.CASCADE if you want to delete students when user is deleted
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER)
    year = models.CharField(max_length=10, choices=YEAR)

    school = models.CharField(max_length=50)
    school_type = models.CharField(max_length=50, choices=SCHOOL_TYPE)
    student_category = models.CharField(max_length=50)
    parent_id = models.ForeignKey(
        Parents, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def __str__(self):
    return f"{self.first_name} {self.last_name}"
