from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from apps.mapview.utils import plzs, get_plzs_close_to
from .tables import StudentTable
from .filters import StudentJobRequirementsFilter

from .forms import StudentForm, EmailToSendForm, EmailForm
from .models import Student, EmailToSend
from apps.accounts.models import User

from apps.ineedstudent.forms import HospitalFormExtra
from apps.ineedstudent.models import Hospital

from match4healthcare.settings.common import MAX_EMAIL_BATCH_PER_HOSPITAL

from django.contrib.auth.decorators import login_required
from apps.accounts.decorator import student_required, hospital_required

from crispy_forms.helper import FormHelper


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
    return render(request, 'thanks.html')


def successful_mail(request):
    return render(request,'emails_sent.html')





@login_required
@hospital_required
def send_mail_student_id_list(request, id_list):
    id_list = id_list.split('_')

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EmailToSendForm(request.POST)

        if form.is_valid():
            # todo check header injections!!!!
            hospital_message = form.cleaned_data['message']



            subject = form.cleaned_data['subject']
            for student_id in id_list:
                student = Student.objects.get(user_id=student_id)

                message = 'Hallo %s %s,\n\n wir haben folgende Nachricht von %s für dich.\n\nDein Match4MedisTeam\n\n%s' % (
                    student.name_first,
                    student.name_last,
                    request.user.hospital.firmenname,
                    hospital_message
                )

                mail = EmailToSend.objects.create(
                    student=student,
                    hospital=request.user.hospital,
                    message=message,
                    subject=subject)
                mail.save()
            if request.user.hospital.is_approved:
                send_mails_for(request.user.hospital)
            return HttpResponseRedirect('/iamstudent/successful_mail')
    else:
        hospital = request.user.hospital
        form = EmailToSendForm(initial={'subject': '[Match4Medis] Ein Ort braucht Deine Hilfe',
                                        'message': 'Liebe Helfer,\n\nWir sind... \nWir suchen...\n\nMeldet euch baldmöglichst!\n\nBeste Grüße,\n%s\n\nTel: %s\nEmail: %s'%(hospital.ansprechpartner,hospital.telefon,hospital.user.email)})

    return render(request, 'send_mail_hospital.html', {'form': form, 'ids': '_'.join(id_list), 'n': len(id_list)})


def send_mails_for(hospital):
    emails = EmailToSend.objects.filter(hospital=hospital, was_sent=False)
    for m in emails:

        if m.subject and m.message and m.student.user.email:

            try:
                send_mail(m.subject,
                          m.message,
                          settings.NOREPLY_MAIL,
                          [m.student.user.email]
                          )
                # todo: muss noch asynchron werden ...celery?
            except BadHeaderError:
                # Do not show error message to malicous actor
                # Do not send the email
                None

            m.was_sent = True
            m.save()


def notify_student(student_id, contact):
    student = Student.objects.get(id=student_id)
    send_mail(subject=_('subject :)'),
              message=_('I want to hire you person of gender %s!, Contact me here: %s') % (student.gender, contact),
              from_email=settings.NOREPLY_MAIL,
              recipient_list=[student.email])

@login_required
@hospital_required
def student_list_view(request, countrycode, plz, distance):
    # only show validated students
    qs = Student.objects.filter(user__validated_email=True)

    # filter by location
    countrycode = request.GET.get('countrycode', countrycode)
    plz = request.GET.get('plz', plz)
    distance = int(request.GET.get('distance', distance))

    if countrycode not in plzs or plz not in plzs[countrycode]:
        return HttpResponse("Postleitzahl: " + plz + " ist keine valide Postleitzahl in " + countrycode)
    lat, lon, ort = plzs[countrycode][plz]
    if distance==0:
        close_plzs=[plz]
    else:
        close_plzs = get_plzs_close_to(countrycode, plz, distance)
    qs = qs.filter(plz__in=close_plzs, countrycode=countrycode)

    # filter by job requirements
    filter_jobrequirements = StudentJobRequirementsFilter(request.GET, queryset=qs)
    qs = filter_jobrequirements.qs

    # displayed table
    table = StudentTable(qs)

    # disable huge amounts of email sends
    enable_mail_send = (filter_jobrequirements.qs.count() <= MAX_EMAIL_BATCH_PER_HOSPITAL)

    # special display to enable the fancy java script stuff and logic
    DISPLAY_filter_jobrequirements = StudentJobRequirementsFilter(request.GET, display_version=True)

    context = {
        'plz': plz,
        'countrycode': countrycode,
        'ort': ort,
        'distance': distance,
        'table': table,
        'filter': DISPLAY_filter_jobrequirements,
        'n': qs.count(),
        'enable_mail': enable_mail_send,
        'max': MAX_EMAIL_BATCH_PER_HOSPITAL
    }

    # saving logic

    uuid = request.GET.get('uuid', '')
    save_filter = request.GET.get('saveFilter', 'false')
    filter_name = request.GET.get('filterName','')

    from .models import StudentListFilterModel, LocationFilterModel
    if save_filter == 'true' and filter_name != '': #todo is valid

        context['filter_is_being_saved'] =True

        # filter has not been saved yet
        loc = LocationFilterModel(plz=plz,distance=distance,countrycode=countrycode)
        student_attr =  dict(request.GET.copy())
        for i in ['plz','distance','countrycode','uuid','saveFilter','filterName']:
            if i in request.GET.keys():
                student_attr.pop(i)

        for i in list(student_attr.keys()):

            if type(student_attr[i]) == list:
                student_attr[i] = student_attr[i][0]

            if student_attr[i] == '':
                student_attr.pop(i)
            elif student_attr[i] == 'true':
                student_attr[i] = True
            elif student_attr[i] == 'false':
                student_attr[i] = False
            else:
                print(student_attr[i])
        print(type(student_attr['ausbildung_typ_mtla']))
        print(student_attr)

        filter_model = StudentListFilterModel(**student_attr,name=filter_name,hospital=request.user.hospital)
        filter_model.save()
        #, location = loc
        context['uuid'] = filter_model.uuid
        context['filter_name'] = filter_model.name

    elif uuid != '':
        # update saved filter
        filter_model = StudentListFilterModel.objects.get(uuid=uuid)
        # todo somehow update attributes
        context['filter_name'] = filter_model.name
        context['uuid'] = filter_model.uuid
        context['filter_is_being_saved'] = True
    else:
        # user does not want to save filter
        context['filter_is_being_saved'] = False






    return render(request, 'student_list_view.html', context)



