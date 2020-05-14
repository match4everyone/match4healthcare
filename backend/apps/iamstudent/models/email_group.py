from datetime import datetime
import uuid

from django.db import models

from apps.ineedstudent.models import Hospital


class EmailGroup(models.Model):
    subject = models.CharField(max_length=200, default="")
    message = models.TextField(default="", max_length=10000)
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
