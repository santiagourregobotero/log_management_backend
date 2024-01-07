from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
from io import BytesIO
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = ('ADMIN', 'Admin')
        USER = ('USER', 'User')

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    role = models.CharField(max_length=255, choices=UserRole.choices, default=UserRole.USER)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email' # login w/ email, unique identifier.
    REQUIRED_FIELDS = [] 

    class Meta:
        db_table = 'auth_user'