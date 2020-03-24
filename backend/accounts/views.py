from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import StudentSignUpForm, HospitalSignUpForm
from .models import User
from ineedstudent.forms import HospitalFormO
from ineedstudent.models import Hospital
from django.shortcuts import render

from iamstudent.forms import StudentForm, StudentFormAndMail
from .forms import StudentEmailForm
from iamstudent.models import Student

from django.contrib.auth.decorators import login_required
# todo: remove email from student and hospital

from .decorator import student_required, hospital_required

from .utils import generate_random_username
from django.contrib.auth.base_user import BaseUserManager

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
            register_student_in_db(request, mail=form.cleaned_data['email'])
            # form.save()
            # redirect to a new URL:
            template = loader.get_template('thanks_student.html')
            return HttpResponse(template.render({}, request))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentFormAndMail()

    return render(request, 'student_signup.html', {'form': form})


@transaction.atomic
def register_student_in_db(request, mail):
    # todo send mail with link to pwd
    pwd = User.objects.make_random_password()
    username = mail  # generate_random_username()
    send_password(username, pwd)
    user = User.objects.create(username=username, is_student=True, email=username)
    user.set_password(pwd)
    user.save()
    h = Student.objects.create(user=user)
    h = StudentForm(request.POST, instance=h)
    h.save()


def send_password(email, pwd):
    send_mail(subject=_('Willkommen bei match4medis'),
              message=_(
                  'Hallo,\n\ndu willst helfen und hast dich gerade bei match4medis registriert, danke!\n\nWenn du deine Daten ändern möchtest, nutze folgende Credentials:\nusername: %s\npasswort: %s\n\nVielen Dank und beste Grüße,\nDein match4medis Team' % (
                  email, pwd)),
              from_email='noreply@medisvs.spahr.uberspace.de',
              # TODO adaptive email adress
              recipient_list=[email])


def hospital_signup(request):
    if request.method == 'POST':
        form_info = HospitalFormO(request.POST)
        form_user = HospitalSignUpForm(request.POST)

        if all([form_info.is_valid(), form_user.is_valid()]):
            register_hospital_in_db(request, form_info.cleaned_data['email'])
            template = loader.get_template('thanks_hospital.html')
            return HttpResponse(template.render({}, request))
    else:
        form_info = HospitalFormO(
            initial={'sonstige_infos': 'Liebe Studis,\n\nwir suchen euch weil ...\n\nBeste Grüße! '})
        form_user = HospitalSignUpForm()
        form_info.helper.form_tag = False

    return render(request, 'hospital_signup.html', {'form_info': form_info, 'form_signup': form_user})


@transaction.atomic
def register_hospital_in_db(request, m):
    u = User.objects.create(username=m)
    user = HospitalSignUpForm(request.POST, instance=u).save()
    h = Hospital.objects.create(user=user)
    h = HospitalFormO(request.POST, instance=h)
    h.save()
from django.contrib import messages

@login_required
@student_required
def edit_student_profile(request):
    student = request.user.student

    if request.method == 'POST':
        form_mail = StudentEmailForm(request.POST, instance=student.user, prefix='account')
        if form_mail.is_valid():
            form_mail.save()
            messages.success(request, 'Your password was updated successfully!', extra_tags='alert')
            form = StudentForm(instance=student, prefix='infos')
        else:
            #todo student form somehow produces an error, but ill fix it later
            form = StudentForm(request.POST, instance=student, prefix='infos')
            form_mail = StudentEmailForm( instance=student.user, prefix='account')
            if form.is_valid():
                form.save()

    else:
        form = StudentForm(instance=student, prefix='infos')
        form_mail = StudentEmailForm(instance=student.user,prefix='account')

    return render(request, 'student_edit.html', {'form': form, 'emailform': form_mail})
