import django_tables2 as tables
from django_tables2 import TemplateColumn

from apps.ineedstudent.models import Hospital


class HospitalTable(tables.Table):
    info = TemplateColumn(template_name="info_button.html")

    class Meta:
        model = Hospital
        template_name = "django_tables2/bootstrap4.html"
        fields = ["firmenname", "ansprechpartner"]
        exclude = ["uuid", "registration_date", "id"]
