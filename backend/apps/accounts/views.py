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

from django.contrib.auth.decorators import login_required
from .decorator import student_required, hospital_required
from django.contrib.admin.views.decorators import staff_member_required



from .utils import generate_random_username
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import BadHeaderError, send_mail

from django.utils.translation import gettext as _
from django.template import loader

from django.http import HttpResponse
from django.db import transaction
from apps.accounts.utils import send_password_set_email


def student_signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentFormAndMail(request.POST)

        # check whether it's valid:
        if form.is_valid():
            user, student = register_student_in_db(request, mail=form.cleaned_data['email'])
            send_password_set_email(
                email=form.cleaned_data['email'],
                host=request.META['HTTP_HOST'],
                subject_template="registration/password_reset_email_subject.txt"
            )
            return HttpResponseRedirect("/iamstudent/thanks")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentFormAndMail()

    return render(request, 'student_signup.html', {'form': form})


@transaction.atomic
def register_student_in_db(request, mail):
    # todo send mail with link to pwd
    pwd = User.objects.make_random_password()
    username = mail  # generate_random_username()
    user = User.objects.create(username=username, is_student=True, email=username)
    user.set_password(pwd)
    user.save()
    student = Student.objects.create(user=user)
    student = StudentForm(request.POST, instance=student)
    student.save()
    #send_password(username, pwd, student.cleaned_data['name_first'])
    return user, student


def hospital_signup(request):
    if request.method == 'POST':
        form_info = HospitalFormInfoSignUp(request.POST)

        if form_info.is_valid():
            user, hospital = register_hospital_in_db(request, form_info.cleaned_data['email'])
            send_password_set_email(
                email=form_info.cleaned_data['email'],
                host=request.META['HTTP_HOST'],
                template="registration/password_set_email_hospital.html",
                subject_template="registration/password_reset_email_subject.txt"
            )
            return HttpResponseRedirect("/iamstudent/thanks")


            #plz = form_info.cleaned_data['plz']
            #countrycode = form_info.cleaned_data['countrycode']
            #distance = 0
            #login(request, user)
            #return HttpResponseRedirect('/ineedstudent/students/%s/%s/%s'%(countrycode,plz,distance))

    else:
        form_info = HospitalFormInfoSignUp(
            initial={'sonstige_infos': 'Liebe Studis,\n\nwir suchen euch weil ...\n\nBeste Grüße! '})
        #form_user = HospitalSignUpForm()
    form_info.helper.form_tag = False
    return render(request, 'hospital_signup.html', {'form_info': form_info })


@transaction.atomic
def register_hospital_in_db(request, m):

    pwd = User.objects.make_random_password()
    user = User.objects.create(username=m, is_hospital=True, email=m)
    user.set_password(pwd)
    print("Saving User")
    user.save()

    hospital = Hospital.objects.create(user=user)
    hospital = HospitalFormInfoCreate(request.POST, instance=hospital)
    print("Saving Hospital")
    hospital.save()
    return user, hospital

from django.contrib import messages


@login_required
def profile_redirect(request):
    user = request.user

    if user.is_student:
        return HttpResponseRedirect('profile_student')

    elif user.is_hospital:
        h = Hospital.objects.get(user=user)
        if not h.datenschutz_zugestimmt or not h.einwilligung_datenweitergabe:
            return HttpResponseRedirect('/ineedstudent/zustimmung')
        return HttpResponseRedirect('profile_hospital')

    elif user.is_staff:
        return HttpResponseRedirect('approve_hospitals')

    else:
        #TODO: throw 404
        HttpResponse('Something wrong in database')

@login_required
def login_redirect(request):
    user = request.user

    if user.is_student:
        return HttpResponseRedirect('/mapview')

    elif user.is_hospital:
        h = Hospital.objects.get(user=user)
        if not h.datenschutz_zugestimmt or not h.einwilligung_datenweitergabe:
            return HttpResponseRedirect('/ineedstudent/zustimmung')
        return HttpResponseRedirect('profile_hospital')

    elif user.is_staff:
        return HttpResponseRedirect('approve_hospitals')

    else:
        #TODO: throw 404
        HttpResponse('Something wrong in database')


@login_required
@student_required
def edit_student_profile(request):
    student = request.user.student

    if request.method == 'POST':
        form = StudentFormEditProfile(request.POST or None, instance=student, prefix='infos')

        if form.is_valid():
            messages.success(request, _('Deine Daten wurden erfolgreich geändert!'), extra_tags='alert-success')
            form.save()

    else:
        form = StudentFormEditProfile(instance=student, prefix='infos')

    return render(request, 'student_edit.html', {'form': form, 'is_activated': student.is_activated})

@login_required
@hospital_required
def edit_hospital_profile(request):
    hospital = request.user.hospital

    if request.method == 'POST':
        form = HospitalFormEditProfile(request.POST or None, instance=hospital, prefix='infos')

        if form.is_valid():
            messages.success(request, _('Deine Daten wurden erfolgreich geändert!'), extra_tags='alert-success')
            form.save()
        else:
            messages.info(request, _('Deine Daten wurden nicht erfolgreich geändert!'), extra_tags='alert-warning')

    else:
        form = HospitalFormEditProfile(instance=hospital, prefix='infos')

    return render(request, 'hospital_edit.html', {'form': form})

@login_required
@staff_member_required
def approve_hospitals(request):
    table_approved = ApprovalHospitalTable(Hospital.objects.filter(is_approved=True))
    table_approved.prefix = 'approved'
    table_approved.paginate(page=request.GET.get(table_approved.prefix + "page", 1), per_page=5)

    table_unapproved = ApprovalHospitalTable(Hospital.objects.filter(is_approved=False))
    table_unapproved.prefix = 'unapproved'
    table_unapproved.paginate(page=request.GET.get(table_unapproved.prefix + "page", 1), per_page=5)

    return render(request, 'approve_hospitals.html', {'table_approved': table_approved, 'table_unapproved': table_unapproved})

@login_required
@staff_member_required
def change_hospital_approval(request,uuid):
    h = Hospital.objects.get(uuid=uuid)
    h.is_approved = not h.is_approved
    h.save()
    if h.is_approved:
        send_mails_for(h)
    return HttpResponseRedirect('/accounts/approve_hospitals')

@login_required
@staff_member_required
def delete_hospital(request,uuid):
    h = Hospital.objects.get(uuid=uuid)
    name = h.user
    h.delete()
    text = format_lazy(_("Du hast die Instiution mit user '{name}' gelöscht."), name=name)
    messages.add_message(request, messages.INFO,text)
    return HttpResponseRedirect('/accounts/approve_hospitals')

@login_required
def delete_me(request):
    user = request.user
    logout(request)
    user.delete()
    return render(request,'deleted_user.html')

@login_required
def delete_me_ask(request):
    user = request.user
    return render(request,'deleted_user_ask.html')

@login_required
def validate_email(request):
    if not request.user.validated_email:
        request.user.validated_email = True
        request.user.save()
    return HttpResponseRedirect("/mapview")


def resend_validation_email(request, email):
    if request.user.is_anonymous:
        if not User.objects.get(username=email).validated_email:
            send_password_set_email(
                email=email,
                host=request.META['HTTP_HOST'],
                template="registration/password_set_email_.html",
                subject_template="registration/password_reset_email_subject.txt"
            )
            return HttpResponseRedirect("/accounts/password_reset/done")
    return HttpResponseRedirect("/")

class UserCountView(APIView):
    """
    A view that returns the count of active users.

    Source: https://stackoverflow.com/questions/25151586/django-rest-framework-retrieving-object-count-from-a-model
    """

    def get(self, request, format=None):
        supporter_count = User.objects.filter( is_student__exact = True, validated_email__exact = True ).count()
        facility_count =  User.objects.filter( is_hospital__exact = True, validated_email__exact = True ).count()
        content = {
            'user_count': supporter_count,
            'facility_count': facility_count
        }
        return JsonResponse(content)


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


@login_required
@student_required
def change_activation_ask(request):
    return render(request, 'change_activation_ask.html',{'is_activated': request.user.student.is_activated})


@login_required
@student_required
def change_activation(request):
    s = request.user.student
    status = s.is_activated
    s.is_activated = not s.is_activated
    s.save()
    if status:
        messages.add_message(request, messages.INFO, _(
            'Du hast dein Profil erfolgreich deaktiviert, du kannst nun keine Anfragen mehr von Hilfesuchenden bekommen.'))
    else:
        messages.add_message(request, messages.INFO,_(
            'Du hast dein Profil erfolgreich aktiviert, du kannst nun wieder von Hilfesuchenden kontaktiert werden.'))
    return HttpResponseRedirect('profile_student')
