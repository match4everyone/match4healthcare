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

from .utils import generate_random_username
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import BadHeaderError, send_mail

from django.utils.translation import gettext as _
from django.template import loader

from django.http import HttpResponse
from django.db import transaction
from apps.accounts.utils import send_password_set_email
from .models import Newsletter, LetterApprovedBy
from .forms import NewsletterEditForm, NewsletterViewForm, TestMailForm

import logging
logger = logging.getLogger(__name__)


def student_signup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        logger.info('Student Signup request', extra={ 'request': request } )
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
        logger.info('Hospital registration request', extra={ 'request': request } )
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
        logger.warning('User is unknown type, profile redirect not possible', extra={ 'request': request } )
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
        return HttpResponseRedirect('/ineedstudent/hospital_dashboard')

    elif user.is_staff:
        return HttpResponseRedirect('approve_hospitals')

    else:
        #TODO: throw 404
        logger.warning('User is unknown type, login redirect not possible', extra={ 'request': request } )
        HttpResponse('Something wrong in database')


@login_required
@student_required
def edit_student_profile(request):
    student = request.user.student

    if request.method == 'POST':
        logger.info('Update Student Profile',extra={ 'request': request })
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
        logger.info('Update Hospital Profile',extra={ 'request': request })
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
    logger.info("Set Hospital {} approval to {}".format(uuid,(not h.is_approved)),extra = { 'request': request })

    if not h.is_approved:
        h.is_approved = True
        h.approval_date = datetime.now()
        h.approved_by = request.user
    else:
        h.is_approved = False
        h.approval_date = None
        h.approved_by = None
    h.save()

    if h.is_approved:
        send_mails_for(h)

    return HttpResponseRedirect('/accounts/approve_hospitals')

@login_required
@staff_member_required
def delete_hospital(request,uuid):
    h = Hospital.objects.get(uuid=uuid)
    logger.info("Delete Hospital {} by {}".format(uuid,request.user),extra = { 'request': request })
    name = h.user
    h.delete()
    text = format_lazy(_("Du hast die Institution mit user '{name}' gelöscht."), name=name)
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
        request.user.email_validation_date = datetime.now()
        request.user.save()
    return HttpResponseRedirect("login_redirect")


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

    def post(self, request, *args, **kwargs):
        logger.info('Login Attempt ({})'.format(request.POST['username']))
        return super().post(request,*args,**kwargs)

    def form_valid(self, form):
        logger.info('Login succesful ({})'.format(form.cleaned_data['username']))
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning('Login failure ({})'.format(form.cleaned_data['username']))
        return super().form_invalid(form)

@login_required
@student_required
def change_activation_ask(request):
    return render(request, 'change_activation_ask.html', {'is_activated': request.user.student.is_activated})


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
        messages.add_message(request, messages.INFO, _(
            'Du hast dein Profil erfolgreich aktiviert, du kannst nun wieder von Hilfesuchenden kontaktiert werden.'))
    return HttpResponseRedirect('profile_student')


def switch_newsletter(nl, user, request, post=None, get=None):
    nl_state = nl.sending_state()

    if nl_state == NewsletterState.BEING_EDITED:
        # an edit was made
        if post is not None:
            form = NewsletterEditForm(post, uuid=nl.uuid, instance=nl)

            if form.is_valid():
                form.save()
                nl.edit_meta_data(user)
                nl.save()
                messages.add_message(request, messages.INFO, _('Bearbeitungen gespeichert.'))
                return switch_newsletter(nl, user, request, post=None, get=None)

        elif get is not None:
            # wants to freeze the form for review
            if 'freezeNewsletter' in get:
                nl.freeze(user)
                nl.save()
                messages.add_message(request, messages.INFO, _(
                    'Der Newsletter kann nun nicht mehr editiert werden. Andere Leute können ihn approven.'))
                return switch_newsletter(nl, user, request, post=None, get=None)
            else:
                # the form is a virgin
                form = NewsletterEditForm(uuid=nl.uuid, instance=nl)
        else:
            form = NewsletterEditForm(uuid=nl.uuid, instance=nl)

    elif nl_state == NewsletterState.UNDER_APPROVAL:
        if get is not None:
            if 'unFreezeNewsletter' in get:
                nl.unfreeze()
                nl.save()
                messages.add_message(request, messages.INFO, _('Der Newsletter kann wieder bearbeitet werden.'))
                return switch_newsletter(nl, user, request, post=None, get=None)
            elif 'approveNewsletter' in get:
                # todo check that author cannot approve
                nl.approve_from(user)
                nl.save()
                messages.add_message(request, messages.WARNING,
                                     format_lazy(_(
                                         'Noch ist deine Zustimmung UNGÜLTIG. Du musst den Validierungslink in der dir gesendeten Mail ({mail}) anklicken.'),
                                         mail=user.email))
                approval = LetterApprovedBy.objects.get(newsletter=nl, user=request.user)
                nl.send_approval_mail(approval, host=request.META['HTTP_HOST'])
                switch_newsletter(nl, user, request, post=None, get=None)

        form = NewsletterViewForm(instance=nl)

    elif nl_state == NewsletterState.READY_TO_SEND:
        if get is not None:
            if 'sendNewsletter' in get:
                nl.send(user)
                nl.save()
                messages.add_message(request, messages.INFO, _('Der Newsletter wurde versendet.'))
                switch_newsletter(nl, user, request)
            if 'unFreezeNewsletter' in get:
                nl.unfreeze()
                nl.save()
                messages.add_message(request, messages.INFO, _('Der Newsletter kann wieder bearbeitet werden.'))
                return switch_newsletter(nl, user, request, post=None, get=None)

        form = NewsletterViewForm(instance=nl)

    elif nl_state == NewsletterState.SENT:
        form = NewsletterViewForm(instance=nl)
    else:
        from django.http import Http404
        raise Http404

    return form, nl


@login_required
@staff_member_required
def view_newsletter(request, uuid):
    # 404 if not there?
    nl = Newsletter.objects.get(uuid=uuid)

    if request.method == 'GET' and 'email' in request.GET:
        email = request.GET.get('email')
        nl.send_testmail_to(email)
        messages.add_message(request, messages.INFO, _('Eine Test Email wurde an %s versendet.' % email))

    post = request.POST if request.method == 'POST' else None
    get = request.GET if request.method == 'GET' else None

    form, nl = switch_newsletter(nl, request.user, request, post=post, get=get)

    # special view if person was the freezer

    context = {
        'form': form,
        'uuid': uuid,
        'newsletter_state': nl.sending_state(),
        'state_enum': NewsletterState,
        'mail_form': TestMailForm(),
        'already_approved_by_this_user': nl.has_been_approved_by(request.user),
        'required_approvals': nl.required_approvals(),
        'frozen_by': nl.frozen_by,
        'sent_by': nl.sent_by,
        'send_date': nl.send_date,
        'approvers': ', '.join([a.user.username for a in nl.letterapprovedby_set.all()])
    }

    return render(request, 'newsletter_edit.html', context)


@login_required
@staff_member_required
def new_newsletter(request):
    newsletter = Newsletter.objects.create()
    newsletter.letter_authored_by.add(request.user)
    newsletter.save()
    return HttpResponseRedirect('view_newsletter/' + str(newsletter.uuid))


from .tables import NewsletterTable


@login_required
@staff_member_required
def list_newsletter(request):
    context = {
        'table': NewsletterTable(Newsletter.objects.all().order_by('-registration_date'))
    }
    return render(request, 'newsletter_list.html', context)


@login_required
@staff_member_required
def did_see_newsletter(request, uuid, token):
    nl = Newsletter.objects.get(uuid=uuid)
    try:
        approval = LetterApprovedBy.objects.get(newsletter=nl, user=request.user)
        if approval.approval_code == int(token):
            approval.did_see_email = True
            approval.save()
            messages.add_message(request, messages.INFO, _('Dein Approval ist nun gültig.'))
        else:
            return HttpResponse('Wrong code')
    except:
        return HttpResponse('Not registered')
    return HttpResponseRedirect('/accounts/view_newsletter/' + str(uuid))
