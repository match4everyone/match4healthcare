# from django.forms import *
from django import forms
from iamstudent.models import Student, EmailToSend
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

    'ba_famulatur': _('Famulatur'),
    'ba_pflegepraktika': _('Pflegepraktika'),
    'ba_fsj_krankenhaus': _('FSJ im Krankenhaus'),

    'skill_coronascreening': _('Corona Screening in der ZINA'),
    'skill_pflegeunterstuetzung': _('Unterstützung der Pflege'),
    'skill_transportdienst': _('Hilfe im Transportdienst'),
    'skill_kinderbetreuung': _('Kinderbetreuung'),
    'skill_labortaetigkeiten': _('generelle Labortätigkeiten'),
    'skill_drkblutspende': _('DRK Blutspende (auch Vorklinik)'),
    'skill_hotline': _('Telefon Hotline'),
    'skill_abstriche': _('Abstriche'),
    'skill_patientenpflege': _('Patientenpflege (Waschen)'),
    'skill_patientenlagerung': _('Patientenlagerung'),
    'skill_opassistenz': _('OP Assistenz'),
    'skill_blutentnahmedienst': _('Blutentnahmedienst'),
    'skill_anrufe': _('Entgegennahme und Bearbeitung von Anrufen Hilfesuchender'),
    'skill_infektionsnachverfolgung': _('Infektionsnachverfolgung'),
    'skill_patientenaufnahme': _('Patientenaufnahme'),
    'skill_edvkenntnisse': _('EDV Kenntnisse'),
    'skill_zugaengelegen': _('Zugänge Legen'),
    'skill_arztbriefeschreiben': _('Arztbriefe schreiben'),
    'skill_blutkulturenabnehmen': _('Blutkulturen abnehmen'),
    'skill_infusionenmischen': _('Infusionen mischen'),
    'skill_ekgschreiben': _('EKG schreiben'),
    'skill_ultraschall': _('Ultraschall'),
    'skill_bgas': _('BGAs'),
    'skill_beatmungsgeraetebedienen': _('Beatmungsgeräte Bedienen'),
}


def create_skills(fields, radio_type):
    rows = []
    col = []
    for f in fields:
        if len(col) == 2:
            rows.append(Row(*col, css_class="form-row"))
            col = []
        c = Column(radio_type(f), css_class='form-group col-md-6 mb-0')
        col.append(c)
    rows.append(Row(*col, css_class="form-row"))
    return rows


def create_radio_traffic_light(field):
    return RadioButtons(field, option_label_class="btn btn-sm btn-light", template='input_buttongroup-traffic_light.html')

def create_radio_progress_indicator(field):
    return RadioButtons(field, option_label_class="btn btn-sm btn-info", template='input_buttongroup-progress_indicator.html')



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
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False
        for field in SKILLS:
            self.fields[field].required = False
        for field in BERUF:
            self.fields[field].required = False
        for field in BERUF2_wo:
            self.fields[field].required = False

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
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('braucht_bezahlung', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            HTML("<h2>{}</h2>".format(_("Berufsausbildung"))),
            HTML("<p>{}</p> <br>".format(_("Bitte gebt hier an, welche Berufsausbildung ihr bereits abgeschlossen oder angefangen habt. Falls ihr eine der Berufsausbildungen nicht angefangen habt, dann müsst ihr nichts weiter angeben."))),
            *create_skills(BERUF, create_radio_progress_indicator),
            Row(*[Column(f, css_class='form-group ') for f in BERUF2_wo],
                css_class='form-row'),
            HTML("<h2>{}</h2>".format(_("Fähigkeiten"))),
                  HTML("<p>{}</p> <br>".format(_("Hier könnt ihr angeben, welche Tätigkeiten und Fähigkeiten ihr beherrscht. Damit können wir den individualisierbarere Suchanfragen für die Hilfesuchenden erstellen. Zudem könnt ihr über das Ampelsystem (rot, gelb, grün) eine Aussage darüber abgeben, wie oft ihr bereits diese Tätigkeit ausgeführt habt."))),
            *create_skills(SKILLS, create_radio_traffic_light),
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
            HTML("<p>{}</p> <br>".format(_(
                "Bitte gebt hier an, welche Berufsausbildung ihr bereits abgeschlossen oder angefangen habt. Falls ihr eine der Berufsausbildungen nicht angefangen habt, dann müsst ihr nichts weiter angeben."))),
            *create_skills(BERUF, create_radio_progress_indicator),
            Row(*[Column(f, css_class='form-group ') for f in BERUF2_wo],
                css_class='form-row'),
            HTML("<h2>{}</h2>".format(_("Fähigkeiten"))),
            HTML("<p>{}</p> <br>".format(_(
                "Hier könnt ihr angeben, welche Tätigkeiten und Fähigkeiten ihr beherrscht. Damit können wir den individualisierbarere Suchanfragen für die Hilfesuchenden erstellen. Zudem könnt ihr über das Ampelsystem (rot, gelb, grün) eine Aussage darüber abgeben, wie oft ihr bereits diese Tätigkeit ausgeführt habt."))),
            *create_skills(SKILLS, create_radio_traffic_light),
            HTML('<p class="text-center">'),
            Submit('submit', _('Eintrag updaten')),
            HTML("</p>")
        )

class EmailToSendForm(forms.ModelForm):

    class Meta:
        model = EmailToSend
        fields = ['subject','message']
        labels = {'subject': _('Betreff'),
                  'message': _('Nachrichtentext')}
        help_texts = {
            'message': _('Hier soll Eure Stellenanzeige stehen, editiert den Text.')
        }
