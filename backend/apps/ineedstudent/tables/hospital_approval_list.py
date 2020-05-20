from django_tables2 import TemplateColumn

from apps.ineedstudent.models import Hospital

from .hospital_list import HospitalTable


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
