import logging

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from apps.accounts.utils import send_password_set_email

logger = logging.getLogger(__name__)


class ParticipantSignupView(View):

    template_signup = None  # "student_signup.html"
    template_thanks_for_registering = None  # "/iamstudent/thanks"
    signup_form = None  # StudentFormAndMail
    save_form = None  # StudentForm
    subject_template = None  # "registration/password_reset_email_subject.txt"
    model = None  # Student
    mail_template = None

    def get(self, request):
        form = self.signup_form()
        return render(request, self.template_signup, {"form": form})

    def post(self, request):
        form = self.signup_form(request.POST)

        if form.is_valid():
            self.register_participant_in_db(request, mail=form.cleaned_data["email"])
            send_password_set_email(
                email=form.cleaned_data["email"],
                host=request.META["HTTP_HOST"],
                subject_template=self.subject_template,
                template=self.mail_template,
            )
            return HttpResponseRedirect(self.template_thanks_for_registering)

        else:
            form = self.signup_form()
            return render(request, self.template_signup, {"form": form})

    @transaction.atomic
    def register_participant_in_db(self, request, mail):
        user = self.model.create_user(mail)
        user.save()

        participant = self.model.objects.create(user=user)
        participant = self.save_form(request.POST, instance=participant)
        participant.save()
        return user, participant
