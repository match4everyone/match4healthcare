from django.forms import *
from apps.ineedstudent.models import Hospital
from django.db import models
from django import forms

from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Row, Column
from apps.accounts.models import User

class HospitalFormO(ModelForm):
    class Meta:
        model = Hospital
        exclude = ['uuid', 'registration_date','user']

        help_texts = {
            'sonstige_infos': _('Einsatzbereiche? Anforderungen? ... und nette Worte :)')
        }

        labels = {
            'plz': _('Postleitzahl'),
            'countrycode': _('Land'),
            'firmenname': _('Name der Institution'),
            'appears_in_map': _('Sichtbar und kontaktierbar für Helfende sein'),
            'sonstige_infos': _('Wichtige Infos über Sie und den potentiellen Einsatzbereich')
        }

    def __init__(self, *args, **kwargs):
        super(HospitalFormO, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'

        self.helper.layout = Layout(
                Row(Column('firmenname') , Column('ansprechpartner')),
  Row(Column('appears_in_map')),
                Row(Column('telefon'), Column('email')),
                Row(Column('plz'), Column('countrycode')),
                'sonstige_infos'
        )



class HospitalForm(HospitalFormO):

    def __init__(self, *args, **kwargs):
        super(HospitalForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Jetzt registrieren',onclick="this.form.submit(); this.disabled=true; this.value='Sending…';"))

class HospitalFormExtra(HospitalFormO):

    def __init__(self, *args, **kwargs):
        super(HospitalFormExtra, self).__init__(*args, **kwargs)
        # !!! namen der knöpe dürfen nicht verändert werden, sonst geht code woanders kaputt
        self.helper.add_input(Submit('submit', _('Schicke Mails')))
        self.helper.add_input(Submit('submit', _('Schicke Mails + Erstelle Anzeige')))

class HospitalFormEditProfile(HospitalFormO):

    def __init__(self, *args, **kwargs):
        super(HospitalFormEditProfile, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', _('Daten aktualisieren'), css_class='btn blue text-white btn-md'))
        self.helper.layout = Layout(
                Row(Column('firmenname') , Column('ansprechpartner')), Row(Column('appears_in_map')),
                Row(Column('telefon')),
                Row(Column('plz'), Column('countrycode')),
                'sonstige_infos'
        )


def check_unique_email(value):
    print("Checking unique email")
    if User.objects.filter(email=value).exists():
        raise ValidationError(_("Diese Email ist bereits vergeben"))
    return value


class HospitalFormInfoSignUp(HospitalFormO):
    email = forms.EmailField(validators=[check_unique_email])

class HospitalFormInfoCreate(HospitalFormO):
    email = forms.EmailField()
