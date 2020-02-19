"""User model module."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from cashier.helpers import file as file_helper
from sorl.thumbnail import ImageField

from .base import BaseModel


class User(AbstractUser, BaseModel):
    """User model."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(_('email address'), unique=True)
    picture = ImageField(upload_to=file_helper.DateUploadPath('buildr/user'),
                         blank=True,
                         null=True)
