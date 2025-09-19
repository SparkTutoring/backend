"""
This is the Models for Students and the Student - Subject - Tutor assignments
"""

from django.db import models
from django.core.exceptions import ValidationError
from utils.choices import GENDER, YEAR, SCHOOL_TYPE
from Parents.models import Parents
from Subjects.models import Subjects
from Tutors.models import Tutors, TutorSubjects


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

    # pylint: disable=too-few-public-methods
    class Meta:
        """  Meta class for Students Model"""
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['year']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentSubjects(models.Model):
    """Extra data for each student’s subject enrollment"""
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    tutor = models.ForeignKey(
        Tutors,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_assignments"
    )
    enrollment_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """ Meta class for StudentSubjects Model """
        verbose_name = 'StudentSubject'
        verbose_name_plural = 'StudentSubjects'
        indexes = [
            models.Index(fields=['student', 'subject']),
        ]
        unique_together = ("student", "subject")

    def __str__(self):
        if self.tutor:
            return f"{self.student} enrolled in {self.subject} with {self.tutor}"
        return f"{self.student} enrolled in {self.subject} (no tutor assigned)"

    def clean(self):
        """Ensure tutor is qualified to teach the subject"""
        # pylint: disable=no-member
        if self.tutor and not TutorSubjects.objects.filter(
            tutor=self.tutor,
            subject=self.subject
        ).exists():
            raise ValidationError(
                f"{self.tutor} is not qualified to teach {self.subject}"
            )
