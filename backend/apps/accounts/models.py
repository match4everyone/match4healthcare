from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    registration_date = models.DateTimeField(default=datetime.now)
    validated_email = models.BooleanField(default=False)
    email_validation_date = models.DateTimeField(blank=True, null=True)
    REQUIRED_FIELDS = ['email']
