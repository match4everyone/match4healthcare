from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView
from django_tables2 import MultiTableMixin
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib import messages

from django.conf import settings
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .forms import StudentSignUpForm, HospitalSignUpForm
from .models import User
from apps.ineedstudent.forms import HospitalFormInfoSignUp, HospitalFormEditProfile, HospitalFormInfoCreate
from apps.ineedstudent.models import Hospital
from django.shortcuts import render
from apps.ineedstudent.views import ApprovalHospitalTable, HospitalTable
from django.contrib import messages
from django.utils.text import format_lazy
from apps.iamstudent.forms import StudentForm, StudentFormEditProfile, StudentFormAndMail
from .forms import StudentEmailForm, HospitalEmailForm, CustomAuthenticationForm
from apps.iamstudent.models import Student
from apps.iamstudent.views import send_mails_for
from .models import NewsletterState

from django.contrib.auth.decorators import login_required
from .decorator import student_required, hospital_required
from django.contrib.admin.views.decorators import staff_member_required

from datetime import datetime

@login_required
@staff_member_required
def view_statistics(request):
    return HttpResponse('Nice')