import django_filters as filters
from .models import Student, BEZAHLUNG_CHOICES, MEDSTUD_CHOICES, AUSBILDUNGS_TYPEN_COLUMNS, BEZAHLUNG_CHOICES_Filter
import django.forms as forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Row, Column, Div, HTML
from crispy_forms.bootstrap import InlineRadios


class StudentJobRequirementsFilter(filters.FilterSet):

    ausbildung_typ_medstud_abschnitt_gt = filters.NumberFilter('ausbildung_typ_medstud_abschnitt',lookup_expr='gte')
    ausbildung_typ_medstud_abschnitt_lt = filters.NumberFilter('ausbildung_typ_medstud_abschnitt', lookup_expr='lte')

    ausbildung_typ_mfa_abschnitt_gt = filters.NumberFilter('ausbildung_typ_mfa_abschnitt',lookup_expr='gte')
    ausbildung_typ_mfa_abschnitt_lt = filters.NumberFilter('ausbildung_typ_mfa_abschnitt',lookup_expr='lte')

    ausbildung_typ_mta_abschnitt_gt = filters.NumberFilter('ausbildung_typ_mta_abschnitt',lookup_expr='gte')
    ausbildung_typ_mta_abschnitt_lt = filters.NumberFilter('ausbildung_typ_mta_abschnitt',lookup_expr='lte')

    ausbildung_typ_mtal_abschnitt_gt = filters.NumberFilter('ausbildung_typ_mtal_abschnitt',lookup_expr='gte')
    ausbildung_typ_mtal_abschnitt_lt = filters.NumberFilter('ausbildung_typ_mtal_abschnitt',lookup_expr='lte')

    ausbildung_typ_notfallsani_abschnitt_gt = filters.NumberFilter('ausbildung_typ_notfallsani_abschnitt',lookup_expr='gte')
    ausbildung_typ_notfallsani_abschnitt_lt = filters.NumberFilter('ausbildung_typ_notfallsani_abschnitt',lookup_expr='lte')

    ausbildung_typ_physio_abschnitt_gt = filters.NumberFilter('ausbildung_typ_physio_abschnitt',lookup_expr='gte')
    ausbildung_typ_physio_abschnitt_lt = filters.NumberFilter('ausbildung_typ_physio_abschnitt',lookup_expr='lte')

    ausbildung_typ_pflege_abschnitt_gt = filters.NumberFilter('ausbildung_typ_pflege_abschnitt',lookup_expr='gte')
    ausbildung_typ_pflege_abschnitt_lt = filters.NumberFilter('ausbildung_typ_pflege_abschnitt',lookup_expr='lte')

    ausbildung_typ_zahni_abschnitt_gt = filters.NumberFilter('ausbildung_typ_zahni_abschnitt',lookup_expr='gte')
    ausbildung_typ_zahni_abschnitt_lt = filters.NumberFilter('ausbildung_typ_zahni_abschnitt',lookup_expr='lte')

    class Meta:
        model = Student
        fields = AUSBILDUNGS_TYPEN_COLUMNS.copy()

        for f in [
            'ausbildung_typ_medstud_famulaturen_anaesthesie',
            'ausbildung_typ_medstud_famulaturen_chirurgie',
            'ausbildung_typ_medstud_famulaturen_innere',
            'ausbildung_typ_medstud_famulaturen_intensiv',
            'ausbildung_typ_medstud_famulaturen_notaufnahme',
            'ausbildung_typ_medstud_anerkennung_noetig'
        ]:
            fields.append(f)

class NamedEmptyFilterSet(filters.FilterSet):

    def __init__(self, *args, **kwargs):
      super(NamedEmptyFilterSet, self).__init__(*args, **kwargs)

      for name, field in self.filters.items():
        if isinstance(field, filters.ChoiceFilter):
              field.extra['choices'] =[(k,v) for k,v in list(field.extra['choices']) if k != '']




class StudentAvailabilityFilter(filters.FilterSet):
    braucht_bezahlung = filters.ChoiceFilter(field_name='braucht_bezahlung', lookup_expr='gte',
                                             choices=BEZAHLUNG_CHOICES_Filter,
                                             label=_('Kann eine Vergütung angeboten werden?'), widget=forms.RadioSelect)
    availability_start = filters.DateFilter(field_name='availability_start', lookup_expr='lte',
                                            label=_('Die Helfenden sollten verfügbar sein ab '))
    unterkunft_gewuenscht = filters.ChoiceFilter(field_name='unterkunft_gewuenscht',
                                                 label=_('Kann eine Unterkunft angeboten werden?'),
                                                 choices=[(True, _('ja')),
                                                          (False, _('nein'))], widget=forms.RadioSelect)

    class Meta:
        model = Student
        fields = {}

    def __init__(self,*args, **kwargs):
        super(StudentAvailabilityFilter, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'availability_start',
            Row(Column(InlineRadios('braucht_bezahlung')),
            Column(InlineRadios('unterkunft_gewuenscht')))
        )
        self.helper.form_tag = False
        self.helper.form_style = 'inline'
