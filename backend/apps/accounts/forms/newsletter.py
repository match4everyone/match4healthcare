from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Layout, Row, Submit
from django import forms
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Newsletter


class BaseNewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = [
            "subject",
            "message",
            "send_to_hospitals",
            "send_to_students",
            "user_validation_required",
        ]
        labels = {
            "send_to_hospitals": _("Institutionen"),
            "send_to_students": _("Helfer*innen"),
            "message": _("Nachricht"),
            "user_validation_required": _("Davon nur an ... Benutzer"),
        }

    def __init__(self, *args, **kwargs):
        super(BaseNewsletterForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f in ["message", "subject"]:
                self.fields[f].label = False
        self.helper = FormHelper()
        self.helper.form_style = "inline"
        self.helper.form_class = "form-inline"

        self.helper.layout = Layout(
            Row(
                Column(HTML(_("<h5>Adressaten</h5>"))),
                Column(
                    Row(HTML(_("Dieser Newsletter geht an"))),
                    Row("send_to_students"),
                    Row("send_to_hospitals"),
                ),
                Column("user_validation_required"),
            ),
            HTML("<hr>"),
            PrependedText("subject", "[match4healthcare]", placeholder=_("Betreff")),
            "message",
        )


class NewsletterEditForm(BaseNewsletterForm):
    def __init__(self, *args, uuid=None, **kwargs):
        super(NewsletterEditForm, self).__init__(*args, **kwargs)
        self.helper.form_id = "id-exampleForm"
        self.helper.form_class = "blueForms"
        self.helper.form_method = "post"
        self.helper.form_action = "/accounts/view_newsletter/" + str(uuid)

        self.helper.attrs = {"onsubmit": "disableButton()"}
        self.helper.add_input(Submit("submit", _("Änderungen Speichern"), css_class="btn-success"))


class NewsletterViewForm(BaseNewsletterForm):
    def __init__(self, *args, **kwargs):
        super(NewsletterViewForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].disabled = True
            self.fields[f].required = False
        self.helper.form_tag = False
