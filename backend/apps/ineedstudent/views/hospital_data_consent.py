import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.accounts.decorator import hospital_required
from apps.ineedstudent.forms import HospitalFormZustimmung

logger = logging.getLogger(__name__)


@method_decorator([login_required, hospital_required], name="dispatch")
class HospitalDataConsent(View):
    def post(self, request):
        h = request.user.hospital
        form_info = HospitalFormZustimmung(request.POST, instance=h)

        if form_info.is_valid():
            h.save()
            return HttpResponseRedirect("/accounts/login_redirect")
        return render(request, "zustimmung.html", {"form_info": form_info})

    def get(self, request):
        form_info = HospitalFormZustimmung()
        return render(request, "zustimmung.html", {"form_info": form_info})
