import django_filters as filters
from .models import Student, BEZAHLUNG_CHOICES, MEDSTUD_CHOICES, AUSBILDUNGS_TYPEN_COLUMNS
import django.forms as forms

class StudentJobRequirementsFilter(filters.FilterSet):
    #name_last = django_filters.CharFilter(lookup_expr='iexact')
    #verfuegbarkeit_ab = filters.DateFromToRangeFilter(field_name='zeitliche_verfuegbarkeit')

    #ausbilguns_arzt = filters.BooleanFilter(field_name='ausbildung_typ_arzt',widget=MyRadioSelect)
    #bla = filters.MultipleChoiceFilter(field_name='ausbildung_typ_arzt_typ',choices=MEDSTUD_CHOICES,widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Student
        fields = AUSBILDUNGS_TYPEN_COLUMNS

class StudentAvailabilityFilter(filters.FilterSet):
    #name_last = django_filters.CharFilter(lookup_expr='iexact')
    #verfuegbarkeit_ab = filters.DateFromToRangeFilter(field_name='zeitliche_verfuegbarkeit')

    #ausbilguns_arzt = filters.BooleanFilter(field_name='ausbildung_typ_arzt',widget=MyRadioSelect)
    bla = filters.MultipleChoiceFilter(field_name='braucht_bezahlung',choices=BEZAHLUNG_CHOICES,widget=forms.CheckboxSelectMultiple)
    avail = filters.DateFilter(field_name='availability_start',lookup_expr='lte')#,widget=forms.DateField)
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
