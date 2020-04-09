from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
import uuid
import numpy as np

ADD_APPROVALS = 1
# todo

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

class NewsletterState:
    SENT = 0
    BEING_EDITED = 1
    UNDER_APPROVAL = 2
    READY_TO_SEND = 3


class Newsletter(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    last_edited_date = models.DateTimeField(default=None, blank=True, null=True)
    frozen_date = models.DateTimeField(default=None, blank=True, null=True)
    send_date = models.DateTimeField(default=None, blank=True, null=True)

    letter_authored_by = models.ManyToManyField(to=User, related_name='letter_authored_by')
    letter_approved_by = models.ManyToManyField(to='User', related_name='letter_approved_by', through='LetterApprovedBy')
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='sent_by')
    frozen_by = models.ForeignKey(User, on_delete=models.SET_NULL,null=True, related_name='frozen_by')

    subject = models.CharField(max_length=200, default='')
    message = models.TextField(default='', max_length=10000)

    was_sent = models.BooleanField(default=False)

    send_to_hospitals = models.BooleanField(default=False)
    send_to_students = models.BooleanField(default=False)

    validation_requirement = models.IntegerField(choices=VALIDATION_CHOICES, default=ONLY_VALIDATED, blank=False)


    def sending_state(self):
        print(self.letter_approved_by)
        if self.was_sent:
            return NewsletterState.SENT
        else:
            if self.frozen_by is None:
                return NewsletterState.BEING_EDITED
            elif LetterApprovedBy.objects.filter(newsletter=self, did_see_email=True).count() < ADD_APPROVALS:
                return NewsletterState.UNDER_APPROVAL
            else:
                return NewsletterState.READY_TO_SEND

def random_number():
    return np.random.randint(0,1000)

class LetterApprovedBy(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter,on_delete=models.CASCADE)
    approval_code = models.IntegerField(default=random_number)
    did_see_email = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'newsletter',)
