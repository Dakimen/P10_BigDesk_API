"""
This file is used to store and access models,
relating to user authentication.

Contains the User model that inherits directly from Abstract User.
Used in this application as the user model.
"""

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import MinValueValidator


class User(AbstractUser):
    """
    User model inheriting from AbstractUser, also includes:
    age - SmallIntegerField with min value of 15
    can_be_contacted - Boolean Field set to false by default
    can_data_be_shared - Boolean Field set to false by default.
    """
    age = models.SmallIntegerField(validators=[MinValueValidator(15)])
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='customauth_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customauth_user'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customauth_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customauth_user'
    )

    def __str__(self):
        return self.username
