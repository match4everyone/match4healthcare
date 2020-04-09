from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
import uuid


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    validated_email = models.BooleanField(default=False)
    email_validation_date = models.DateTimeField(blank=True, null=True)
    REQUIRED_FIELDS = ['email']


ONLY_VALIDATED = 0
ONLY_NOT_VALIDATED = 1
ALL = 2

VALIDATION_CHOICES = (
    (ONLY_VALIDATED, 'only validated'),
    (ONLY_NOT_VALIDATED, 'only not validated'),
    (ALL, 'validated and not validated'),
)


class Newsletter(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    authored_by = models.ManyToManyField(to=User, related_name='authored_by')
    approved_by = models.ManyToManyField(to=User, related_name='approved_by')
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL)

    subject = models.CharField(max_length=200, default='')
    message = models.TextField(default='', max_length=10000)

    was_sent = models.BooleanField(default=False)

    send_to_hospitals = models.BooleanField(default=False)
    send_to_students = models.BooleanField(default=False)

    validation_requirement = models.IntegerField(choices=VALIDATION_CHOICES, default=ONLY_VALIDATED, blank=False)
