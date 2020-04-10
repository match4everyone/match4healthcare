from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.core.mail import EmailMessage
from django.conf import settings

import uuid
import numpy as np


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
    (ONLY_VALIDATED, 'validierte'),
    (ONLY_NOT_VALIDATED, 'nicht validierte'),
    (ALL, 'varlidierte und nicht validierte'),
)


class NewsletterState:
    BEING_EDITED = 1
    UNDER_APPROVAL = 2
    READY_TO_SEND = 3
    SENT = 4


class Newsletter(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    registration_date = models.DateTimeField(default=datetime.now, blank=True, null=True)
    last_edited_date = models.DateTimeField(default=None, blank=True, null=True)
    frozen_date = models.DateTimeField(default=None, blank=True, null=True)
    send_date = models.DateTimeField(default=None, blank=True, null=True)

    letter_authored_by = models.ManyToManyField(to=User, related_name='letter_authored_by')
    letter_approved_by = models.ManyToManyField(to='User', related_name='letter_approved_by',
                                                through='LetterApprovedBy')
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_by')
    frozen_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='frozen_by')

    subject = models.CharField(max_length=200, default='')
    message = models.TextField(default='', max_length=10000)

    was_sent = models.BooleanField(default=False)

    send_to_hospitals = models.BooleanField(default=False)
    send_to_students = models.BooleanField(default=False)

    user_validation_required = models.IntegerField(choices=VALIDATION_CHOICES, default=ONLY_VALIDATED, blank=False)

    def sending_state(self):
        if self.was_sent:
            return NewsletterState.SENT
        else:
            if self.frozen_by is None:
                return NewsletterState.BEING_EDITED
            elif self.required_approvals() > 0:
                return NewsletterState.UNDER_APPROVAL
            else:
                return NewsletterState.READY_TO_SEND

    def unfreeze(self):
        self.frozen_by = None
        self.frozen_date = None
        LetterApprovedBy.objects.filter(newsletter=self).delete()

    def approve_from(self, user):
        self.letter_approved_by.add(user)

    def send(self, user):
        self.send_date = datetime.now()
        self.was_sent = True
        self.sent_by = user

    def freeze(self, user):
        self.frozen_by = user
        self.frozen_date = datetime.now()

    def edit_meta_data(self, user):
        self.letter_authored_by.add(user)
        self.last_edited_date = datetime.now()

    def send_testmail_to(self, email_receipient):
        email = EmailMessage(
            subject=self._subject(),
            body=self.message,
            from_email=settings.NOREPLY_MAIL,
            to=[email_receipient]
        )
        email.content_subtype = "html"
        email.send()

    def has_been_approved_by(self, user):
        return LetterApprovedBy.objects.filter(newsletter=self, user=user, did_see_email=True).count() == 1

    def required_approvals(self):
        return settings.NEWSLETTER_REQUIRED_APPROVERS - LetterApprovedBy.objects.filter(newsletter=self,
                                                                                        did_see_email=True).count()

    def send_approval_mail(self, approval, host):
        body = '<h3>Link zum Approven ganz unten</h3><hr>'
        body += self.message
        body += '<hr><a href="https://%s/accounts/view_newsletter/%s"> Ich habe Probleme gefunden und will den ' \
                'Newsletter bearbeiten.</a><br>' \
                % (host, self.uuid)
        body += '<a href="https://%s">Ich bestätige, dass diese E-Mail als Newsletter' \
                ' abgeschickt werden darf.</a>' \
                % approval.verify_url(host)
        email = EmailMessage(
            subject=self._subject(),
            body=body,
            from_email=settings.NOREPLY_MAIL,
            to=[approval.user.email]
        )
        email.content_subtype = "html"
        email.send()

    def _subject(self):
        return '[match4healthcare] ' + str(self.subject)


def random_number():
    return np.random.randint(0, 100000)


class LetterApprovedBy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    approval_code = models.IntegerField(default=random_number)
    did_see_email = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'newsletter',)

    def verify_url(self, host):
        return '%s/accounts/did_see_newsletter/%s/%s' % (host, self.newsletter.uuid, self.approval_code)
