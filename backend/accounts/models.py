from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    #username = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']