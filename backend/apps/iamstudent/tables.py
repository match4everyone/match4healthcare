import django_tables2 as tables
from .models import Student
from django_tables2 import TemplateColumn

class StudentTable(tables.Table):
    info = TemplateColumn(template_name='info_button.html')
    select = TemplateColumn(template_name='checkbox_studenttable.html')

    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap4.html"
        exclude = ['uuid','registration_date','id']
        fields = ['user']