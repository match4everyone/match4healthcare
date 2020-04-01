import django_tables2 as tables
from .models import Student
from django_tables2 import TemplateColumn
from django.utils.html import format_html


class StudentTable(tables.Table):
    select = tables.TemplateColumn(template_name='checkbox_studenttable.html',visible=False)
    select.attrs = {'td': {
        'class': "bs-checkbox",
        'id': lambda record: 'display-table-%s' % record.user_id}}

    detail_view = tables.TemplateColumn('<a target="_blank" href="/iamstudent/view_student/{{record.uuid}}">Details</a>')

    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap4.html"
        exclude = ['uuid', 'registration_date', 'id']
        fields = ['plz','sonstige_qualifikationen','unterkunft_gewuenscht','zeitliche_verfuegbarkeit','braucht_bezahlung']
        attrs = {
            'data-toggle': "table",
            'data-search': "false",
            'data-filter-control': "true",
            'data-show-export': "false",
            'data-click-to-select': "true",
            'data-toolbar': "#toolbar",
            'class': "table table-sm"
        }
        row_attrs = {
            "data-id": lambda record: record.user_id
        }

    def render_name_first(self, record):
        return format_html("%s %s." % (record.name_first, record.name_last[0:1]))
