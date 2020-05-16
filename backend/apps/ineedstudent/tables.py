from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
import django_tables2 as tables
from django_tables2 import TemplateColumn

from apps.iamstudent.models import Student
from apps.ineedstudent.models import Hospital


class StudentTable(tables.Table):
    info = TemplateColumn(template_name="info_button.html")
    checkbox = TemplateColumn(template_name="checkbox_studenttable.html")

    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap4.html"
        exclude = ["uuid", "registration_date", "id"]
        fields = ["user"]


class ContactedTable(tables.Table):
    registration_date = tables.Column(verbose_name=_("E-Mail versendet am"))
    is_activated = tables.Column(empty_values=(), verbose_name=_("Helfer*in noch verfügbar"))
    details = tables.TemplateColumn(template_name="modal_button.html", verbose_name=_(""))

    # TODO: add link to student detail view to button # noqa: T003
    # student_info = tables.TemplateColumn(template_name='student_info_button.html',verbose_name=_(''))

    def render_is_activated(self, value):
        if value:
            text = _("ja")
        else:
            text = _("nein")
        return format_html('<div class="text-center">{}</div>'.format(text))


class HospitalTable(tables.Table):
    info = TemplateColumn(template_name="info_button.html")

    class Meta:
        model = Hospital
        template_name = "django_tables2/bootstrap4.html"
        fields = ["firmenname", "ansprechpartner"]
        exclude = ["uuid", "registration_date", "id"]


class ApprovalHospitalTable(HospitalTable):
    info = TemplateColumn(template_name="info_button.html")
    status = TemplateColumn(template_name="approval_button.html")
    delete = TemplateColumn(template_name="delete_button.html")

    class Meta:
        model = Hospital
        template_name = "django_tables2/bootstrap4.html"
        fields = [
            "firmenname",
            "ansprechpartner",
            "user",
            "telefon",
            "plz",
            "user__validated_email",
            "approval_date",
            "approved_by",
        ]
        exclude = ["uuid", "id", "registration_date"]
