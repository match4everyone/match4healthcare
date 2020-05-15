import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View

from apps.accounts.decorator import hospital_required, student_required
from apps.iamstudent.forms import StudentFormEditProfile
from apps.iamstudent.models import Student
from apps.ineedstudent.forms import HospitalFormEditProfile
from apps.ineedstudent.models import Hospital

logger = logging.getLogger(__name__)


# TODO: refactor the required decorators to the model # noqa:T003


class ParticipantEditProfileView(View):
    model = None  # Hospital, Student
    edit_form = None  # HospitalFormEditProfile, StudentFormEditProfile
    template = None  # "hospital_edit.html"

    # decorate dispatch with login required, specific user required

    def get_user_from_request(self, request):
        return None

    def get(self, request):

        participant = self.get_user_from_request(request)

        form = self.edit_form(instance=participant, prefix="infos")

        return render(request, self.template, {"form": form, "participant": participant})

    def post(self, request):

        participant = self.get_user_from_request(request)

        form = self.edit_form(request.POST or None, instance=participant, prefix="infos")

        if form.is_valid():
            logger.info("Update %s profile", self.model.__name__, extra={"request": request})
            messages.success(
                request, _("Deine Daten wurden erfolgreich geändert!"), extra_tags="alert-success",
            )
            form.save()
        else:
            messages.info(
                request,
                _("Deine Daten wurden nicht erfolgreich geändert!"),
                extra_tags="alert-warning",
            )

        return render(request, self.template, {"form": form, "participant": participant})


@method_decorator([login_required, hospital_required], name="dispatch")
class HospitalEditProfileView(ParticipantEditProfileView):
    model = Hospital
    edit_form = HospitalFormEditProfile
    template = "hospital_edit.html"

    def get_user_from_request(self, request):
        return request.user.hospital


@method_decorator([login_required, student_required], name="dispatch")
class StudentEditProfileView(ParticipantEditProfileView):
    model = Student
    edit_form = StudentFormEditProfile
    template = "student_edit.html"

    def get_user_from_request(self, request):
        return request.user.student
