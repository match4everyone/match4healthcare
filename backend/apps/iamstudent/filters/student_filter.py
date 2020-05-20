from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, HTML, Layout, Row
from django import forms
from django.utils.translation import gettext_lazy as _
import django_filters as filters

from apps.iamstudent.forms.student import button_group_filter, form_labels
from apps.iamstudent.models import Student
from apps.iamstudent.models.student import (
    AUSBILDUNGS_IDS,
    AUSBILDUNGS_TYPEN,
    AUSBILDUNGS_TYPEN_COLUMNS,
    BEZAHLUNG_CHOICES_Filter,
)


class StudentJobRequirementsFilter(filters.FilterSet):

    ausbildung_typ_medstud_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_medstud_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_medstud_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_medstud_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_mfa_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_mfa_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_mfa_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_mfa_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_mta_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_mta_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_mta_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_mta_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_ota_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_ota_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_ota_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_ota_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_ata_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_ata_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_ata_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_ata_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_mtla_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_mtla_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_mtla_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_mtla_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_notfallsani_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_notfallsani_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_notfallsani_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_notfallsani_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_physio_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_physio_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_physio_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_physio_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_ergotherapie_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_ergotherapie_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_ergotherapie_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_ergotherapie_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_psycho_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_psycho_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_psycho_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_psycho_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_pflege_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_pflege_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_pflege_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_pflege_abschnitt", lookup_expr="lte"
    )

    ausbildung_typ_zahni_abschnitt_x_gt = filters.NumberFilter(
        "ausbildung_typ_zahni_abschnitt", lookup_expr="gte"
    )
    ausbildung_typ_zahni_abschnitt_x_lt = filters.NumberFilter(
        "ausbildung_typ_zahni_abschnitt", lookup_expr="lte"
    )

    braucht_bezahlung = filters.ChoiceFilter(
        field_name="braucht_bezahlung",
        lookup_expr="gte",
        choices=BEZAHLUNG_CHOICES_Filter,
        label=_("Kann eine Vergütung angeboten werden?"),
        widget=forms.RadioSelect,
    )
    availability_start = filters.DateFilter(
        field_name="availability_start",
        lookup_expr="lte",
        label=_("Die Helfenden sollten verfügbar sein ab "),
    )
    unterkunft_gewuenscht = filters.ChoiceFilter(
        field_name="unterkunft_gewuenscht",
        label=_("Kann eine Unterkunft angeboten werden?"),
        choices=[(True, _("ja")), (False, _("nein"))],
        widget=forms.RadioSelect,
    )

    unterkunft_gewuenscht.field.empty_label = _("wissen wir nicht")
    braucht_bezahlung.field.empty_label = _("wissen wir nicht")

    class Meta:
        model = Student
        fields = AUSBILDUNGS_TYPEN_COLUMNS.copy()

        for f in [
            "ausbildung_typ_medstud_famulaturen_anaesthesie",
            "ausbildung_typ_medstud_famulaturen_allgemeinmedizin",
            "ausbildung_typ_medstud_famulaturen_chirurgie",
            "ausbildung_typ_medstud_famulaturen_innere",
            "ausbildung_typ_medstud_famulaturen_intensiv",
            "ausbildung_typ_medstud_famulaturen_notaufnahme",
            "ausbildung_typ_medstud_anerkennung_noetig",
            "ausbildung_typ_kinderbetreung_ausgebildet_abschnitt",
        ]:
            fields.append(f)

    def __init__(self, *args, **kwargs):
        if "display_version" not in kwargs.keys():
            display_version = False
        else:
            display_version = True
            del kwargs["display_version"]

        super(StudentJobRequirementsFilter, self).__init__(*args, **kwargs)

        self.Meta.labels = form_labels
        self.Meta.labels["unterkunft_gewuenscht"] = _("Kann eine Unterkunft angeboten werden?")

        THREE_CHOICES = [("true", "notwendig")]

        if display_version:
            for a_field in self.form.fields.keys():
                approved = self.form.fields[a_field]

                if type(approved) is forms.NullBooleanField:
                    self.form.fields[a_field] = forms.MultipleChoiceField(
                        choices=THREE_CHOICES, required=False, widget=forms.CheckboxSelectMultiple,
                    )
                if type(approved) is forms.DecimalField:
                    basename = a_field.split("_x_")[0]
                    CHOICES = self.Meta.model._meta._forward_fields_map[basename].choices
                    from copy import deepcopy

                    if a_field.split("_x_")[1] == "gt":
                        CHOICES_GT = list(deepcopy(CHOICES))
                        CHOICES_GT[0] = ("", _("Egal"))
                        self.form.fields[a_field] = forms.TypedChoiceField(
                            choices=CHOICES_GT, required=False
                        )
                        self.form.fields[a_field].initial = 0
                    else:
                        CHOICES_LT = list(deepcopy(CHOICES))
                        CHOICES_LT[0] = ("", _("Egal"))
                        self.form.fields[a_field] = forms.TypedChoiceField(
                            choices=CHOICES_LT, required=False
                        )
                        self.form.fields[a_field].initial = 10

                if a_field in form_labels.keys():
                    self.form.fields[a_field].label = form_labels[a_field]

            self.form_helper = get_form_helper_filter()


def get_form_helper_filter():
    helper = FormHelper()
    helper.form_id = "id-exampleForm"
    helper.form_class = "blueForms"
    helper.form_method = "get"

    helper.form_action = "submit_survey"
    helper.form_style = "inline"
    helper.layout = Layout(
        Div(
            Row(
                *[
                    Column(
                        "ausbildung_typ_%s" % k.lower(),
                        css_class="ausbildung-checkbox form-group col-md-6 mb-0",
                        css_id="ausbildung-checkbox-%s" % AUSBILDUNGS_IDS[k],
                    )
                    for k in AUSBILDUNGS_TYPEN.keys()
                ]
            ),
            css_id="div-berufsausbildung-dropdown",
        )
    )

    for ausbildungstyp, felder in AUSBILDUNGS_TYPEN.items():
        if len(felder) != 0:
            if ausbildungstyp != "MEDSTUD":
                helper.layout.extend(
                    [
                        Div(
                            HTML(
                                "<hr><h5>Zusätzliche Filter zu {}</h5>".format(
                                    _(form_labels["ausbildung_typ_%s" % ausbildungstyp.lower()])
                                )
                            ),
                            Row(
                                *[
                                    Column(
                                        button_group_filter(
                                            "ausbildung_typ_%s_%s"
                                            % (ausbildungstyp.lower(), f.lower())
                                        ),
                                        css_class="form-group",
                                        css_id=f.replace("_", "-"),
                                    )
                                    for f in felder.keys()
                                    if "ausbildung_typ_medstud_abschnitt"
                                    == "ausbildung_typ_%s_%s" % (ausbildungstyp.lower(), f.lower())
                                ]
                            ),
                            *[
                                Column(
                                    button_group_filter(
                                        "ausbildung_typ_%s_%s" % (ausbildungstyp.lower(), f.lower())
                                    ),
                                    css_class="form-group col-md-6 mb-0",
                                    css_id=f.replace("_", "-"),
                                )
                                for f in felder.keys()
                                if "ausbildung_typ_medstud_abschnitt"
                                != "ausbildung_typ_%s_%s" % (ausbildungstyp.lower(), f.lower())
                            ],
                            css_id="div-ausbildung-%s" % AUSBILDUNGS_IDS[ausbildungstyp],
                            css_class="hidden ausbildung-addon",
                        )
                    ]
                )
            else:
                helper.layout.extend(
                    [
                        Div(
                            HTML(
                                "<hr><h5>Zusätzliche Filter zu {}</h5>".format(
                                    _(form_labels["ausbildung_typ_%s" % ausbildungstyp.lower()])
                                )
                            ),
                            Row(
                                *[
                                    Column(
                                        button_group_filter(
                                            "ausbildung_typ_%s_%s"
                                            % (ausbildungstyp.lower(), f.lower())
                                        ),
                                        css_class="form-group",
                                        css_id=f.replace("_", "-"),
                                    )
                                    for f in felder.keys()
                                    if "ausbildung_typ_medstud_abschnitt"
                                    == "ausbildung_typ_%s_%s" % (ausbildungstyp.lower(), f.lower())
                                ]
                            ),
                            HTML("<p>"),
                            HTML(
                                _(
                                    "In welchen der folgenden Bereiche sind Vorerfahrungen notwendig?"
                                )
                            ),
                            HTML("</p>"),
                            *[
                                Column(
                                    button_group_filter(
                                        "ausbildung_typ_%s_%s" % (ausbildungstyp.lower(), f.lower())
                                    ),
                                    css_class="form-group col-md-6 mb-0",
                                    css_id=f.replace("_", "-"),
                                )
                                for f in felder.keys()
                                if "ausbildung_typ_medstud_abschnitt"
                                != "ausbildung_typ_%s_%s" % (ausbildungstyp.lower(), f.lower())
                            ],
                            css_id="div-ausbildung-%s" % AUSBILDUNGS_IDS[ausbildungstyp],
                            css_class="hidden ausbildung-addon",
                        )
                    ]
                )

    helper.form_tag = False
    helper.layout.extend(
        [
            HTML("<hr><h5>"),
            HTML(_(" Welche Infos über die zu vergebende Stelle sind schon bekannt?")),
            HTML("</h5>"),
            "availability_start",
            Row(
                Column(InlineRadios("braucht_bezahlung")),
                Column(InlineRadios("unterkunft_gewuenscht")),
            ),
        ]
    )
    return helper
