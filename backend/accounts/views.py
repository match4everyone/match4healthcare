from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .forms import StudentSignUpForm, HospitalSignUpForm
from .models import User
from ineedstudent.forms import HospitalFormO
from ineedstudent.models import Hospital
from django.shortcuts import render

from iamstudent.forms import StudentForm
from iamstudent.models import Student

from .utils import generate_random_username
from django.contrib.auth.base_user import BaseUserManager

from django.http import HttpResponse
from django.db import transaction

def student_signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            register_student_in_db(request)
            #form.save()
            # redirect to a new URL:
            return HttpResponse('thanks')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'student_signup.html', {'form': form})

@transaction.atomic
def register_student_in_db(request):
    print('khkjhj')
    pwd = BaseUserManager().make_random_password()
    username = generate_random_username()
    user = User.objects.create(username=username,password=pwd)
    h = Student.objects.create(user=user)
    h = StudentForm(request.POST, instance=h)
    h.save()



def hospital_signup(request):
    if request.method == 'POST':
        form_info = HospitalFormO(request.POST)
        form_user = HospitalSignUpForm(request.POST)

        if all([form_info.is_valid(), form_user.is_valid()]):
            register_hospital_in_db(request)
            return HttpResponse('registered both of you')
    else:
        form_info = HospitalFormO(initial={'sonstige_infos': 'Liebe Studis,\n\nwir suchen euch weil ...\n\nBeste Grüße! '})
        form_user = HospitalSignUpForm()
        form_info.helper.form_tag = False


    return render(request, 'hospital_signup.html', {'form_info': form_info, 'form_signup': form_user})

@transaction.atomic
def register_hospital_in_db(request):
    user = HospitalSignUpForm(request.POST).save()
    h = Hospital.objects.create(user=user)
    h = HospitalFormO(request.POST, instance=h)
    h.save()