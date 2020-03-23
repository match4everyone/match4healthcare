from django.forms import *
from ineedstudent.models import Hospital
from django.db import models

from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper

from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, HTML, Row, Column

class HospitalFormO(ModelForm):
    class Meta:
        model = Hospital
        exclude = ['uuid', 'registration_date']

        help_texts = {
            'sonstige_infos': _('Einsatzbereiche? Anforderungen? ... und nette Worte :)')
        }

        labels = {
            'plz': _('Postleitzahl'),
            'countrycode': _('Land'),
            'firmenname': _('Name der Institution'),
            'sonstige_infos': _('Wichtige Infos über Euch und den potentiellen Einsatzbereich')
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
                Row(Column('telefon'), Column('email')),
                Row(Column('plz'), Column('countrycode')),
                'sonstige_infos'
        )



class HospitalForm(HospitalFormO):

    def __init__(self, *args, **kwargs):
        super(HospitalForm, self).__init__(*args, **kwargs)
        self.helper.add_input(Submit('submit', 'Registriere Mich'))

class HospitalFormExtra(HospitalFormO):

    def __init__(self, *args, **kwargs):
        super(HospitalFormExtra, self).__init__(*args, **kwargs)
        # !!! namen der knöpe dürfen nicht verändert werden, sonst geht code woanders kaputt
        self.helper.add_input(Submit('submit', 'Schicke Mails'))
        self.helper.add_input(Submit('submit', 'Schicke Mails + Erstelle Anzeige'))
