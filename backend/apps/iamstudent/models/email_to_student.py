from datetime import datetime
import uuid

from django.db import models

from apps.ineedstudent.models import Hospital

from . import EmailGroup, Student


# emails that hospitals send to students
class EmailToSend(models.Model):

    subject = models.CharField(max_length=200, default="")
    message = models.TextField(default="", max_length=10000)
    was_sent = models.BooleanField(default=False)

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)

    send_date = models.DateTimeField(null=True)

    email_group = models.ForeignKey(EmailGroup, on_delete=models.CASCADE, null=True, blank=True)
