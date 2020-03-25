from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView


from matchmedisvsvirus.settings.common import NOREPLY_MAIL
from .forms import StudentSignUpForm, HospitalSignUpForm
from .models import User
from ineedstudent.forms import HospitalFormInfoSignUp, HospitalFormEditProfile
from ineedstudent.models import Hospital
from django.shortcuts import render
from ineedstudent.views import ApprovalHospitalTable, HospitalTable

from iamstudent.forms import StudentForm, StudentFormEditProfile, StudentFormAndMail
from .forms import StudentEmailForm, HospitalEmailForm
from iamstudent.models import Student
from iamstudent.views import send_mails_for

from django.contrib.auth.decorators import login_required
from .decorator import student_required, hospital_required
from django.contrib.admin.views.decorators import staff_member_required



from .utils import generate_random_username
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import BadHeaderError, send_mail

from django.utils.translation import gettext as _
from django.template import loader

from django.http import HttpResponse
from django.db import transaction


def student_signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentFormAndMail(request.POST)

        # check whether it's valid:
        if form.is_valid():
            user, student = register_student_in_db(request, mail=form.cleaned_data['email'])
            send_password_set_email(form.cleaned_data['email'], request.META['HTTP_HOST'])
            return HttpResponseRedirect("/iamstudent/thanks")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentFormAndMail()

    return render(request, 'student_signup.html', {'form': form})


def send_password_set_email(email, host, template='registration/password_reset_email_.html'):
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        form.save(email_template_name=template, domain_override=host)

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


def send_password(email, pwd, name):
    send_mail(subject=_('Willkommen bei match4healthcare'),
              message=_(
                  'Hallo %s,\n\ndu willst helfen und hast dich gerade bei match4healthcare registriert, danke!\n\nWenn du deine Daten ändern möchtest, nutze folgende Credentials:\nusername: %s\npasswort: %s\n\nVielen Dank und beste Grüße,\nDein match4healthcare Team' % (
                  name, email, pwd)),
              from_email=NOREPLY_MAIL,
              # TODO adaptive email adress
              recipient_list=[email])


def hospital_signup(request):
    if request.method == 'POST':
        form_info = HospitalFormInfoSignUp(request.POST)
        form_user = HospitalSignUpForm(request.POST)

        if all([form_info.is_valid(), form_user.is_valid()]):
            user, hospital = register_hospital_in_db(request, form_info.cleaned_data['email'])
            plz = form_info.cleaned_data['plz']
            countrycode = form_info.cleaned_data['countrycode']
            distance = 0
            login(request, user)
            return HttpResponseRedirect('/ineedstudent/students/%s/%s/%s'%(countrycode,plz,distance))

    else:
        form_info = HospitalFormInfoSignUp(
            initial={'sonstige_infos': 'Liebe Studis,\n\nwir suchen euch weil ...\n\nBeste Grüße! '})
        form_user = HospitalSignUpForm()
    form_info.helper.form_tag = False
    return render(request, 'hospital_signup.html', {'form_info': form_info, 'form_signup': form_user})


@transaction.atomic
def register_hospital_in_db(request, m):
    u = User.objects.create(username=m)
    user = HospitalSignUpForm(request.POST, instance=u).save()
    hospital = Hospital.objects.create(user=user)
    hospital = HospitalFormInfoSignUp(request.POST, instance=hospital)
    hospital.save()
    return user, hospital

from django.contrib import messages

@login_required
def login_redirect(request):
    user = request.user

    if user.is_student:
        return HttpResponseRedirect('profile_student')

    elif user.is_hospital:
        return HttpResponseRedirect('profile_hospital')

    elif user.is_staff:
        return HttpResponseRedirect('approve_hospitals')

    else:
        #todo: throw 404
        HttpResponse('Something wrong in database')


@login_required
@student_required
def edit_student_profile(request):
    student = request.user.student

    if not request.user.validated_email:
        request.user.validated_email = True
        request.user.save()

    if request.method == 'POST':
        form_mail = StudentEmailForm(request.POST or None, instance=student.user, prefix='account')
        if 'account-email' in request.POST and form_mail.is_valid():
            form_mail.save()
            messages.success(request, _('Deine Email wurde erfolgreich geändert!'), extra_tags='alert-success')
            form = StudentFormEditProfile(instance=student, prefix='infos')
        else:
            form = StudentFormEditProfile(request.POST or None, instance=student, prefix='infos')
            messages.success(request, _('Deine Daten wurden erfolgreich geändert!'), extra_tags='alert-success')
            form_mail = StudentEmailForm( instance=student.user, prefix='account')

            if form.is_valid():
                form.save()

    else:
        form = StudentFormEditProfile(instance=student, prefix='infos')
        form_mail = StudentEmailForm(instance=student.user,prefix='account')

    return render(request, 'student_edit.html', {'form': form, 'emailform': form_mail})

@login_required
@hospital_required
def edit_hospital_profile(request):
    hospital = request.user.hospital

    if request.method == 'POST':
        form_mail = HospitalEmailForm(request.POST or None, instance=request.user, prefix='account')
        if 'account-email' in request.POST and form_mail.is_valid():
            form_mail.save()
            messages.success(request, _('Deine Email wurde erfolgreich geändert!'), extra_tags='alert-success')
            form = HospitalFormEditProfile(instance=hospital, prefix='infos')
        else:
            form = HospitalFormEditProfile(request.POST or None, instance=hospital, prefix='infos')
            messages.success(request, _('Deine Daten wurden erfolgreich geändert!'), extra_tags='alert-success')
            form_mail = HospitalEmailForm( instance=request.user, prefix='account')

            if form.is_valid():
                form.save()

    else:
        form = HospitalFormEditProfile(instance=hospital, prefix='infos')
        form_mail = HospitalEmailForm(instance=request.user,prefix='account')

    return render(request, 'hospital_edit.html', {'form': form, 'emailform': form_mail})

@login_required
@staff_member_required
def approve_hospitals(request):
    table_approved = ApprovalHospitalTable(Hospital.objects.filter(is_approved=True))
    table_approved.paginate(page=request.GET.get("page", 1), per_page=5)
    table_unapproved = ApprovalHospitalTable(Hospital.objects.filter(is_approved=False))
    table_unapproved.paginate(page=request.GET.get("page", 1), per_page=5)
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
def delete_me(request):
    user = request.user
    logout(request)
    user.delete()
    return render(request,'deleted_user.html')
