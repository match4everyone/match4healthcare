import django_tables2 as tables
from .models import Student
from django_tables2 import TemplateColumn
from django.utils.html import format_html

class StudentTable(tables.Table):
    select = TemplateColumn(template_name='checkbox_studenttable.html')
    #info = TemplateColumn(template_name='info_button.html')

    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap4.html"
        exclude = ['uuid','registration_date','id']
        fields = ['name_first']

    def render_name_first(self, record):
        return format_html("%s %s." % (record.name_first, record.name_last[0:1]))