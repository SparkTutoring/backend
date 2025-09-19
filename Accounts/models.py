"""  
This is the Models for Accounts to change the default user model
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group,
    Permission
)
from django.utils.translation import gettext_lazy as _
from utils.choices import ROLES


class CustomUserManager(BaseUserManager):
    """Custom user model manages email as the identifiers for authentication"""

    def create_user(self, email, password=None, **extra_fields):
        """ Create and save a User with the given email and password """
        if not email:
            raise ValueError('Email must be provided')

        email = self.normalize_email(email)
        email = email.lower()

        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """ Create and save a SuperUser with the given email and password """
        # For superusers, don't require a school
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        # School will be set to None in the save method

        user = self.create_user(email, password, **extra_fields)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that supports using email instead of username """
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=50, choices=ROLES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Specify custom related_name for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_groups',  # Custom reverse relationship name
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions',  # Custom reverse relationship name
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        # pylint: disable=too-few-public-methods
        """ Meta class to provide ordering and verbose names """
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['email']

    def __str__(self):
        return str(self.email) if self.email else ""
