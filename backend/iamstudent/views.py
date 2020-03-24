from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .forms import StudentForm, EmailForm
from .models import Student

from ineedstudent.forms import HospitalFormExtra
from ineedstudent.models import Hospital

from django.contrib.auth.decorators import login_required
from accounts.decorator import student_required, hospital_required



def get_student(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('thanks')


    # if a GET (or any other method) we'll create a blank form
    else:
        form = StudentForm()

    return render(request, 'student.html', {'form': form})


def thx(request):
    return render(request, 'thanks_student.html')


def successful_mail(requets):
    return HttpResponse("Mail was sent :)")


def send_mail_student(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            notify_student(form.cleaned_data['student_id'], form.cleaned_data['contact_adress'])

            return HttpResponseRedirect('successful_mail')

    else:
        form = EmailForm()
    return render(request, 'mail.html', {'form': form})

@login_required
@hospital_required
def send_mail_student_id_list(request, id_list):
    id_list = id_list.split('_')
    # existierende anzeige benutzen

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HospitalFormExtra(request.POST)

        # check whether it's valid:
        if form.is_valid():
            submit = request.POST.get('submit')


            message = 'Hey! \n  %s, Contact me here: %s \n %s' % (form.cleaned_data['sonstige_infos'],
                                                            form.cleaned_data['ansprechpartner'],
                                                            form.cleaned_data['email'])

            for student_id in id_list:
                student = Student.objects.get(id=student_id)
                contact =form.cleaned_data['email']

                # TODO: Demo
                #send_mail(subject=_('[Name der App] Offered a job.'),
                #          message=message,
                #          from_email='noreply@medisvs.spahr.uberspace.de',
                #          recipient_list=[student.email])
            if 'Erstelle Anzeige' in submit:
                form.save()
                return HttpResponse('Dies ist noch eine Demo. Im Release-Programm wären emails jetzt erfolgreich verschickt und eine dauerhafte Anzeige gespeichert.')
                #TODO Demo
                #return HttpResponse('mails geschickt und anzeige gestellt')
            else:
                return HttpResponse('Dies ist noch eine Demo. Im Release-Programm wären emails jetzt erfolgreich verschickt')
                #TODO Demo
                #return HttpResponse('mails geschickt und KEINE anzeige gestellt')

        # if a GET (or any other method) we'll create a blank form
    else:
        form = HospitalFormExtra()

    return render(request, 'send_mail_hospital.html', {'form': form, 'ids': '_'.join(id_list), 'n': len(id_list)})

def notify_student(student_id, contact):
    student = Student.objects.get(id=student_id)
    send_mail(subject=_('subject :)'),
              message=_('I want to hire you person of gender %s!, Contact me here: %s') % (student.gender, contact),
              from_email='noreply@medisvs.spahr.uberspace.de',
              recipient_list=[student.email])
