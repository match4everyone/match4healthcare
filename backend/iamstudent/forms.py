# from django.forms import *
from django import forms
from iamstudent.models import Student
from django.db import models

from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column, Div, HTML
from crispy_forms.bootstrap import InlineRadios
from iamstudent.custom_crispy import RadioButtons

SKILLS = ['skill_coronascreening', 'skill_pflegeunterstuetzung', 'skill_transportdienst', 'skill_kinderbetreuung',
          'skill_labortaetigkeiten', 'skill_drkblutspende', 'skill_hotline', 'skill_abstriche', 'skill_patientenpflege',
          'skill_patientenlagerung', 'skill_opassistenz', 'skill_blutentnahmedienst', 'skill_anrufe',
          'skill_infektionsnachverfolgung',
          'skill_patientenaufnahme', 'skill_edvkenntnisse', 'skill_zugaengelegen', 'skill_arztbriefeschreiben',
          'skill_blutkulturenabnehmen', 'skill_infusionenmischen', 'skill_ekgschreiben', 'skill_ultraschall',
          'skill_bgas',
          'skill_beatmungsgeraetebedienen']

BERUF = [
    'ba_arzt', 'ba_krankenpflege', 'ba_pflegehilfe', 'ba_anaesthesiepflege', 'ba_intensivpflege', 'ba_ota', 'ba_mfa',
     'ba_mta_lta', 'ba_rta', 'ba_rettungssanitaeter', 'ba_kinderbetreuung', 'ba_hebamme', 'ba_sprechstundenhilfe',
     'ba_labortechnische_assistenz']
BERUF2_wo = ['ba_famulatur', 'ba_pflegepraktika', 'ba_fsj_krankenhaus']

form_labels = {
    'uuid': _('Writer'),
    'registration_date': _('Writer'),

    'name_first': _('Vorname'),
    'name_last': _('Nachname'),
    'phone_number': _('Telefonnummer'),

    'plz': _('Wohnort'),
    'countrycode': _('Land'),
    'email': _('Email'),

    'semester': _('Semester'),
    'immatrikuliert': _('Ich bin aktuell immatrikuliert'),
    'availability_start': _('Ich bin verfügbar ab'),

    'braucht_bezahlung': _('Ich benötige eine Vergütung'),

    'famulaturreife': _('Famulaturreife'),
    'm2absolviert': _('M2 absolviert'),
    'berufserfahrung_monate': _('Berufserfahrung in Monaten'),

    'ba_arzt': _('Arzt/Ärztin'),
    'ba_krankenpflege': _('Pfleger*in'),
    'ba_pflegehilfe': _('Pflegehelfer*in'),
    'ba_anaesthesiepflege': _('Anästhesiepfleger*in'),
    'ba_intensivpflege': _('Intensivpfleger*in'),
    'ba_ota': _('OTA'),
    'ba_mfa': _('MFA'),
    'ba_mta_lta': _('MTA/LTA'),
    'ba_rta': _('RTA'),
    'ba_rettungssanitaeter': _('Rettungssanitäter*in'),
    'ba_kinderbetreuung': _('Kinderbetreuer*in'),
    'ba_hebamme': _('Hebamme'),
    'ba_sprechstundenhilfe': _('Sprechstundenhilfe'),
    'ba_labortechnische_assistenz': _('Labortechnische Assistenz'),

}


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['uuid', 'registration_date','user']
        labels = form_labels
        help_texts = {
            'availability_start': _('Bitte ein Datum im Format YYYY-MM-DD, also zB 2020-03-21'),
            'email': _('Über diese Emailadresse dürfen dich medizinische Einrichtungen kontaktieren'),
            'plz': _('Bitte gib deine Postleitzahl ein'),
            'countrycode': _('Bitte wähle ein Land aus'),
            'ba_famulatur': _('in Monaten'),
            'ba_pflegepraktika': _('in Monaten'),
            'ba_fsj_krankenhaus': _('in Monaten'),
            'plz': _('bevorzugter Einsatzort'),
            'wunsch_ort_gesundheitsamt': _('Hotline, Teststation etc.'),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        #for field in SKILLS:
        #    self.fields[field].required = False
        #for field in BERUF:
        #    self.fields[field].required = False
        #for field in BERUF2_wo:
        #    self.fields[field].required = False

        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.layout = Layout(
            Row(
                Column('name_first', css_class='form-group col-md-6 mb-0'),
                Column('name_last', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),


            HTML("<h2>{}</h2>".format(_("Einsatz"))),
            Row(
                Column('plz', css_class='form-group col-md-4 mb-0'),
                Column('countrycode', css_class='form-group col-md-4 mb-0'),
                Column('umkreis', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('availability_start', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            HTML("<h5>{}</h5>".format(_("Wunscheinsatzort"))),
            Row(
                Column('wunsch_ort_arzt', css_class='form-group col-md-6 mb-0'),
                Column('wunsch_ort_gesundheitsamt', css_class='form-group col-md-6 mb-0'),
                Column('wunsch_ort_krankenhaus', css_class='form-group col-md-6 mb-0'),
                Column('wunsch_ort_pflege', css_class='form-group col-md-6 mb-0'),
                Column('wunsch_ort_rettungsdienst', css_class='form-group col-md-6 mb-0'),
                Column('wunsch_ort_labor', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('braucht_bezahlung', css_class='form-group col-md-6 mb-0'),
                Column('zeitliche_verfuegbarkeit', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Div(                
                HTML("<h2>{}</h2>".format(_("Berufsausbildung"))),
                css_id='div-berufsausbildung-dropdown',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("Arzt Felder"))),
                css_id='div-ausbildung-1',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("Medizinstudent Felder"))),
                css_id='div-ausbildung-2',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("MFA Felder"))),
                css_id='div-ausbildung-3',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("MTA Felder"))),
                css_id='div-ausbildung-4',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("MTLA Felder"))),
                css_id='div-ausbildung-5',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("NOTFALLSANI Felder"))),
                css_id='div-ausbildung-6',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("PFLEGESTUD Felder"))),
                css_id='div-ausbildung-7',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("SANI Felder"))),
                css_id='div-ausbildung-8',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("ZAHNI Felder"))),
                css_id='div-ausbildung-9',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("Kinderbetreuung Felder"))),
                css_id='div-ausbildung-10',
                css_class='hidden',
            ),
            Div(
                HTML("<h2>{}</h2>".format(_("Sonstige Felder"))),
                css_id='div-ausbildung-11',
                css_class='hidden',
            ),

            HTML('<p class="text-center">'),
            Submit('submit', 'Registriere Mich'),
            HTML("</p>")
        )

class StudentFormAndMail(StudentForm):
    email = forms.EmailField()


class EmailForm(forms.Form):
    student_id = forms.CharField(max_length=100)
    contact_adress = forms.EmailField()


class StudentFormEditProfile(StudentForm):
    def __init__(self, *args, **kwargs):
        super(StudentFormEditProfile, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('name_first', css_class='form-group col-md-6 mb-0'),
                Column('name_last', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('plz', css_class='form-group col-md-6 mb-0'),
                Column('countrycode', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('availability_start', css_class='form-group col-md-6 mb-0'),
                Column('semester', css_class='form-group col-md-4 mb-0'),
                Column('immatrikuliert', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('braucht_bezahlung', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML("<h2>{}</h2>".format(_("Berufsausbildung"))),
            # TODO: alle neuen felder hier auch hinzufügen!!!!!
            HTML('<p class="text-center">'),
            Submit('submit', _('Eintrag updaten')),
            HTML("</p>")
        )