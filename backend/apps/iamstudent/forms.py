# from django.forms import *
from django import forms
from apps.iamstudent.models import Student, EmailToSend, AUSBILDUNGS_DETAIL_COLUMNS,AUSBILDUNGS_TYPEN, AUSBILDUNGS_TYPEN_COLUMNS, AUSBILDUNGS_IDS, PersistenStudentFilterModel
from django.db import models
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Field, Row, Column, Div, HTML
from crispy_forms.bootstrap import InlineRadios
from apps.iamstudent.custom_crispy import RadioButtons
from apps.accounts.models import User
from crispy_forms.bootstrap import InlineRadios

import logging

form_labels = {
    'uuid': _('Writer'),
    'registration_date': _('Writer'),

    'name_first': _('Vorname'),
    'name_last': _('Nachname'),
    'phone_number': _('Telefonnummer'),

    'plz': _('Postleitzahl'),
    'countrycode': _('Land'),
    'email': _('Email'),

    'semester': _('Semester'),
    'immatrikuliert': _('Ich bin aktuell immatrikuliert'),
    'availability_start': _('Ich bin verfügbar ab'),

    'braucht_bezahlung': _('Ich benötige eine Vergütung'),

    # Form Labels for qualifications
    'ausbildung_typ_pflege': _('Pflege <em>(melde Dich auch bei <a href="https://pflegereserve.de/#/login">Pflegereserve</a>)</em>'),
    'ausbildung_typ_pflege_abschnitt': _('Ausbildungsabschnitt'),
    'ausbildung_typ_physio': _('Physiotherapeut_in'),
    'ausbildung_typ_physio_abschnitt': _('Ausbildungsabschnitt'),
    'ausbildung_typ_hebamme': _('Entbindungshelfer_in'),
    'ausbildung_typ_fsj': _('FSJ im Gesundheitswesen'),
    'ausbildung_typ_arzt': _('Arzt/Ärztin'),
    'ausbildung_typ_arzt_typ': _('Fachbereich'),
    'ausbildung_typ_arzt_sonstige': _('Sonstige:'),
    'ausbildung_typ_medstud': _('Medizinstudent_in'),
    'ausbildung_typ_medstud_abschnitt': _('Ausbildungsabschnitt'),
    'ausbildung_typ_medstud_farmulaturen_anaesthesie': _('Famulatur Anästhesie'),
    'ausbildung_typ_medstud_famulaturen_chirurgie': _('Famulatur Chirurgie'),
    'ausbildung_typ_medstud_famulaturen_innere': _('Famulatur Innere'),
    'ausbildung_typ_medstud_famulaturen_intensiv': _('Famulatur Intensivmedizin'),
    'ausbildung_typ_medstud_famulaturen_notaufnahme': _('Famulatur Notaufnahme'),
    'ausbildung_typ_medstud_anerkennung_noetig': _(
        'Eine Anerkennung als Teil eines Studienabschnitts (Pflegepraktikum/Famulatur) ist wichtig'),
    'ausbildung_typ_mfa': _('Medizinische_r Fachangestellte_r'),
    'ausbildung_typ_mfa_abschnitt': _('Ausbildungsabschnitt'),
    'ausbildung_typ_mtla': _('Medizinisch-technische_r Laboratoriumsassistent_in'),
    'ausbildung_typ_mtla_abschnitt': _('Ausbildungsabschnitt'),
    'ausbildung_typ_mta': _('Medizinisch-technische_r Assistent_in'),
    'ausbildung_typ_mta_abschnitt': _('Ausbildungsabschnitt'),
    'ausbildung_typ_notfallsani': _('Notfallsanitäter_in/Rettungssanitäter_in'),
    'ausbildung_typ_notfallsani_abschnitt': _('Ausbildungsabschnitt'),
    'ausbildung_typ_sani': _('Rettungssanitäter_in/Rettungshelfer_in'),
    'ausbildung_typ_zahni': _('Zahnmedizinstudent_in'),
    'ausbildung_typ_zahni_abschnitt': _('Ausbildungsabschnitt'),
    'ausbildung_typ_kinderbetreung': _('Kinderbetreuer_in'),
    'ausbildung_typ_kinderbetreung_ausgebildet': _('Abgeschlossene Ausbildung'),
    'ausbildung_typ_kinderbetreung_vorerfahrung': _('Lediglich Erfahrungen'),
    'ausbildung_typ_sonstige': _('Sonstige'),
    'ausbildung_typ_sonstige_eintragen': _('Bitte die Qualifikationen hier eintragen'),
    'datenschutz_zugestimmt': _('Hiermit akzeptiere ich die Datenschutzbedingungen.'),
    'einwilligung_datenweitergabe': _(
        'Ich bestätige, dass meine Angaben korrekt sind und ich der Institution meinen Ausbildungsstand nachweisen kann. Mit der Weitergabe meiner Kontaktdaten an die Institutionen bin ich einverstanden.'),
    'wunsch_ort_arzt': _('Arztpraxis/Ordination'),
    'wunsch_ort_gesundheitsamt': _('Gesundheitsamt'),
    'wunsch_ort_krankenhaus': _('Krankeneinrichtungen'),
    'wunsch_ort_pflege': _('Pflegeeinrichtungen'),
    'wunsch_ort_rettungsdienst': _('Rettungsdienst'),
    'wunsch_ort_labor': _('Labor'),
}
fields_for_button_group = ['ausbildung_typ_arzt_typ',
'ausbildung_typ_pflege_abschnitt',
                           'ausbildung_typ_physio_abschnitt',
                           'ausbildung_typ_medstud_abschnitt',
                           'ausbildung_typ_mfa_abschnitt',
                           'ausbildung_typ_mtla_abschnitt',
                           'ausbildung_typ_mta_abschnitt',
                           'ausbildung_typ_notfallsani_abschnitt',
                           'ausbildung_typ_zahni_abschnitt']


def button_group(field):
    if 'empty' in field:
        return Column()
    if field in fields_for_button_group:
        return ButtonGroup(field)
    return field


def ButtonGroup(field):
    return RadioButtons(field, option_label_class="btn btn-sm btn-light",
                        template='input_buttongroup-any_indicator.html')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['uuid', 'registration_date', 'user']
        labels = form_labels
        help_texts = {
            'email': _('Über diese Emailadresse dürfen dich medizinische Einrichtungen kontaktieren'),
            'countrycode': _('Bitte wähle ein Land aus'),
            'plz': _('bevorzugter Einsatzort als Postleitzahl'),
           # 'wunsch_ort_gesundheitsamt': _('Hotline, Teststation etc.')
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = False

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
                Row(*[Column('ausbildung_typ_%s' % k.lower(), css_class='ausbildung-checkbox form-group col-md-6 mb-0',
                             css_id='ausbildung-checkbox-%s' % AUSBILDUNGS_IDS[k]) for k in
                      AUSBILDUNGS_TYPEN.keys()]),
                css_id='div-berufsausbildung-dropdown',
            ),
            *[
                Div(
                    HTML("<h4>{}</h4>".format(_(form_labels['ausbildung_typ_%s' % ausbildungstyp.lower()]))),
                    Row(*[
                        Column(button_group('ausbildung_typ_%s_%s' % (ausbildungstyp.lower(), f.lower())),
                               css_class='form-group col-md-6 mb-0', css_id=f.replace('_', '-'))
                        for f in felder.keys()
                    ]), css_id='div-ausbildung-%s' % AUSBILDUNGS_IDS[ausbildungstyp]
                    , css_class='hidden'
                )
                for ausbildungstyp, felder in AUSBILDUNGS_TYPEN.items() if len(felder) != 0
            ]
            ,
            HTML('<hr>'),
            HTML('<p class="text-left">'),
            'datenschutz_zugestimmt',
            HTML("</p>"),
            HTML('<p class="text-left">'),
            'einwilligung_datenweitergabe',
            HTML("</p>"),
            HTML('<p class="text-center">'),
            Submit('submit', 'Registriere mich', css_class='btn blue text-white btn-md'),
            HTML("</p>")
        )

        logging.debug(self.helper.layout)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Diese Email ist bereits vergeben"))
        return email


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

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("Diese Email ist bereits vergeben"))
        return email


class EmailToSendForm(forms.ModelForm):
    class Meta:
        model = EmailToSend
        fields = ['subject', 'message']
        labels = {'subject': _('Betreff'),
                  'message': _('Nachrichtentext')}
        help_texts = {
            'message': _('Hier soll Eure Stellenanzeige stehen, editiert den Text.')
        }

class PersistenStudentFilterForm(forms.ModelForm):
    #executions = ['%s = forms.NullBooleanField(widget=MyRadioSelect)' % a for a in  AUSBILDUNGS_TYPEN_COLUMNS]
    #for e in executions:
    #    exec(e)



    class Meta:
        model = PersistenStudentFilterModel

        labels = form_labels
        exclude = ['hospital']
        #widgets = {
        #    AUSBILDUNGS_TYPEN_COLUMNS[0]: MyRadioSelect
        #}

    def __init__(self, *args, **kwargs):
        super(PersistenStudentFilterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'get'

        self.helper.form_action = 'submit_survey'
        self.helper.form_style = 'inline'
        for k in AUSBILDUNGS_DETAIL_COLUMNS:
            self.fields[k].required = False
        self.helper.layout = Layout(
            #Row(*[Column(Field(a,widget=MyRadioSelect), css_class='form-group col-md-6 mb-0') for a in AUSBILDUNGS_TYPEN_COLUMNS])
            Div(
                HTML("<h2>{}</h2>".format(_("Berufsausbildung"))),
                Row(*[Column(ButtonGroup('ausbildung_typ_%s' % k.lower()), css_class='ausbildung-checkbox form-group col-md-6 mb-0',
                             css_id='ausbildung-checkbox-%s' % AUSBILDUNGS_IDS[k]) for k in
                      AUSBILDUNGS_TYPEN.keys()]),
                css_id='div-berufsausbildung-dropdown',
            ),
            # todo einblenden der anderen felder
            *[
                Div(
                    HTML("<h4>{}</h4>".format(_(form_labels['ausbildung_typ_%s' % ausbildungstyp.lower()]))),
                    Row(*[
                        Column(button_group('ausbildung_typ_%s_%s' % (ausbildungstyp.lower(), f.lower())),
                               css_class='form-group col-md-6 mb-0', css_id=f.replace('_', '-'))
                        for f in felder.keys()
                    ]), css_id='div-ausbildung-%s' % AUSBILDUNGS_IDS[ausbildungstyp]
                    , css_class='hidden'
                )
                for ausbildungstyp, felder in AUSBILDUNGS_TYPEN.items() if len(felder) != 0
            ]
        )
        self.helper.add_input(Submit('submit', _('Aktualisieren')))
        print(self.helper.layout)

