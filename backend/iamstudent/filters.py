import django_filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
    name_last = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Student
        fields = ['name_last', 'name_first']