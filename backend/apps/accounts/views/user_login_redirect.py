import logging

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.ineedstudent.models import Hospital

logger = logging.getLogger(__name__)


@method_decorator([login_required], name="dispatch")
class LoginRedirect(View):
    def get(self, request):
        user = request.user

        if user.is_student:
            return HttpResponseRedirect("/mapview")

        elif user.is_hospital:
            h = Hospital.objects.get(user=user)
            if not h.datenschutz_zugestimmt or not h.einwilligung_datenweitergabe:
                return HttpResponseRedirect("/ineedstudent/zustimmung")
            return HttpResponseRedirect("/ineedstudent/hospital_dashboard")

        elif user.is_staff:
            return HttpResponseRedirect("profile_staff")

        else:
            logger.warning(
                "User is unknown type, login redirect not possible", extra={"request": request},
            )
            return Http404
