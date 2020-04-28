from django import forms
from apps.evaluation.models import StudentEvaluation, InstitutionEvaluation
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, HTML, Row

from apps.evaluation.custom_crispy import RadioButtons


def make_button_group(field):
    return RadioButtons(field, option_label_class="btn btn-md blue text-white",
                        template='evaluation/input_buttongroup-any_indicator.html')


class StudentEvaluationForm(forms.ModelForm):
    class Meta:
        model = StudentEvaluation
        exclude = []

        labels = {
            'overall_rating': _('Bitte bewerte deine Erfahrung mit match4healthcare insgesamt!'),
            'registration_feedback': _('Hier hast du die Möglichkeit, uns allgemeines Feedback zum match4healthcare'
                                       ' zu geben.'),
            'suggested_improvements': _('Falls du Verbesserungsvorschläge hast, dann kannst du sie hier loswerden'),
            'likelihood_recommendation': _('Wie hoch ist die Wahrscheinlichkeit, dass du unsere Seite weiterbwerten'
                                           'wirst?'),
            'contact_mail': _('Hier kannst du deine Mail da lassen, falls du uns für Rückfragen zur Verfügung stehen '
                              'möchtest'),
            'communication_with_institutions': _('Wie lief für dich die Kommunikation mit den Institutionen?'),
        }

        widgets = {
            'registration_feedback': forms.Textarea(attrs={'rows': 4}),
            'communication_with_institutions': forms.Textarea(attrs={'rows': 4}),
            'suggested_improvements': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentEvaluationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'student'

        self.helper.layout = Layout(
            make_button_group('overall_rating'),
            'registration_feedback',
            'communication_with_institutions',
            'suggested_improvements',
            make_button_group('likelihood_recommendation'),
            'contact_mail',
        )

    def clean_overall_rating(self):
        if not self.cleaned_data['overall_rating']:
            raise forms.ValidationError(_('Bitte gib eine Gesamtbewertung ab!'), code='invalid')
        return True
