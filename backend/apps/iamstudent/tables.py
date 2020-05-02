import django_tables2 as tables
from .models import Student
from django_tables2 import TemplateColumn
from django.utils.html import format_html
from django.utils.translation import gettext as _


class StudentTable(tables.Table):
    select = tables.TemplateColumn(
        template_name="checkbox_studenttable.html", visible=False
    )
    select.attrs = {
        "td": {
            "class": "bs-checkbox",
            "id": lambda record: "display-table-%s" % record.user_id,
        }
    }
    detail_view = tables.TemplateColumn(
        '<a target="_blank" href="/iamstudent/view_student/{{record.uuid}}">Details</a>'
    )

    def __init__(self, *args, **kwargs):
        for c, n in self.Meta.verbose_name.items():
            self.base_columns[c].verbose_name = n
        self.hospital = kwargs["hospital"]
        del kwargs["hospital"]
        super().__init__(*args, **kwargs)

    class Meta:
        model = Student
        template_name = "django_tables2/bootstrap4.html"
        exclude = ["uuid", "registration_date", "id"]
        fields = [
            "emailtosend_set",
            "plz",
            "sonstige_qualifikationen",
            "zeitliche_verfuegbarkeit",
            "unterkunft_gewuenscht",
            "braucht_bezahlung",
        ]
        attrs = {
            "data-toggle": "table",
            "data-search": "false",
            "data-filter-control": "true",
            "data-show-export": "false",
            "data-click-to-select": "true",
            "data-toolbar": "#toolbar",
            "class": "table table-sm",
        }
        row_attrs = {"data-id": lambda record: record.user_id}
        verbose_name = {
            "plz": _("Postleitzahl"),
            "emailtosend_set": _("Kontaktiert"),
            "sonstige_qualifikationen": _("Sonst. Qualifikationen"),
            "unterkunft_gewuenscht": _("Braucht Unterkunft"),
            "zeitliche_verfuegbarkeit": _("Verfügbarkeit"),
            "braucht_bezahlung": _("Bezahlung Notwendig"),
        }

    def render_name_first(self, record):
        return format_html("%s %s." % (record.name_first, record.name_last[0:1]))

    def render_emailtosend_set(self, record):
        # check if it had been contacted before
        value = record.emailtosend_set.filter(hospital=self.hospital).count()
        if value > 0:
            return "✔"
        else:
            return "✘"

    def render_braucht_bezahlung(self, value):
        if "freue" in value:
            return "✘"
        else:
            return "✔"
