import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from apps.accounts.decorator import hospital_required
from apps.iamstudent.forms import StudentFormView
from apps.iamstudent.models import Student

logger = logging.getLogger(__name__)


@method_decorator([login_required, hospital_required], name="dispatch")
class StudentDetailView(View):
    def get(self, request):
        s = Student.objects.get(uuid=self.kwargs["uuid"])
        form = StudentFormView(instance=s, prefix="infos")
        context = {"form": form}
        return render(request, "view_student.html", context)
