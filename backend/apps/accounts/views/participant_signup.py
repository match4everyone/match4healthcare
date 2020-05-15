import logging

from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from apps.accounts.utils import send_password_set_email

logger = logging.getLogger(__name__)


class ParticipantSignupView(View):

    template_signup = None  # template used for the signup dialog
    template_thanks_for_registering = None  # template to redirect to after successful signup
    signup_form = None  # form that should be displayed for signup
    save_form = None  # form that should be used for saving
    subject_template = None  # template for password reset email
    model = None  # model that should be signed up
    mail_template = None  # template for the email body

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
