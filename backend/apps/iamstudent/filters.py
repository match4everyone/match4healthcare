import django_filters as filters
from .models import Student, BEZAHLUNG_CHOICES, MEDSTUD_CHOICES, AUSBILDUNGS_TYPEN_COLUMNS, ARZT_CHOICES
import django.forms as forms

class StudentJobRequirementsFilter(filters.FilterSet):

    ausbildung_typ_arzt_typ = filters.MultipleChoiceFilter('ausbildung_typ_arzt_typ',choices=ARZT_CHOICES,widget=forms.CheckboxSelectMultiple)


    ausbildung_typ_medstud_abschnitt = filters.NumberFilter('ausbildung_typ_medstud_abschnitt',lookup_expr='gte')
    ausbildung_typ_mfa_abschnitt = filters.NumberFilter('ausbildung_typ_mfa_abschnitt',lookup_expr='gte')
    ausbildung_typ_mta_abschnitt = filters.NumberFilter('ausbildung_typ_mta_abschnitt',lookup_expr='gte')
    ausbildung_typ_mtal_abschnitt = filters.NumberFilter('ausbildung_typ_mtal_abschnitt',lookup_expr='gte')
    ausbildung_typ_notfallsani_abschnitt = filters.NumberFilter('ausbildung_typ_notfallsani_abschnitt',lookup_expr='gte')
    ausbildung_typ_physio_abschnitt = filters.NumberFilter('ausbildung_typ_physio_abschnitt',lookup_expr='gte')
    ausbildung_typ_pflege_abschnitt = filters.NumberFilter('ausbildung_typ_pflege_abschnitt',lookup_expr='gte')
    ausbildung_typ_zahni_abschnitt = filters.NumberFilter('ausbildung_typ_zahni_abschnitt',lookup_expr='gte')

    class Meta:
        model = Student
        fields = AUSBILDUNGS_TYPEN_COLUMNS.copy()
        fields.append('ausbildung_typ_arzt_typ')

        for f in [
            'ausbildung_typ_medstud_famulaturen_anaesthesie',
            'ausbildung_typ_medstud_famulaturen_chirurgie',
            'ausbildung_typ_medstud_famulaturen_innere',
            'ausbildung_typ_medstud_famulaturen_intensiv',
            'ausbildung_typ_medstud_famulaturen_notaufnahme',
            'ausbildung_typ_medstud_anerkennung_noetig'
        ]:
            fields.append(f)


class StudentAvailabilityFilter(filters.FilterSet):
    #name_last = django_filters.CharFilter(lookup_expr='iexact')
    #verfuegbarkeit_ab = filters.DateFromToRangeFilter(field_name='zeitliche_verfuegbarkeit')

    #ausbilguns_arzt = filters.BooleanFilter(field_name='ausbildung_typ_arzt',widget=MyRadioSelect)
    bla = filters.MultipleChoiceFilter(field_name='braucht_bezahlung',choices=BEZAHLUNG_CHOICES,widget=forms.CheckboxSelectMultiple)
    availability_start = filters.DateFilter(field_name='availability_start',lookup_expr='lte')#,widget=forms.DateField)
    class Meta:
        model = Student
        fields ={
            #'price': ['lt', 'gt'],
            #'availability_start': ['exact']#'date__gt'],
        }


"""
class NarrowStudentFilter(filters.FilterSet):

    class Meta:
        model = Student
        fields = []

    def __init__(self):
        super(NarrowStudentFilter).__init__()
"""
