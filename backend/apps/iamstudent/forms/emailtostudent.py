from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.iamstudent.models import EmailToSend


class EmailToSendForm(forms.ModelForm):
    class Meta:
        model = EmailToSend
        fields = ["subject", "message"]
        labels = {"subject": _("Betreff"), "message": _("Nachrichtentext")}
        help_texts = {}

    def clean_message(self):
        message = self.cleaned_data["message"]
        initial_message = self.initial["message"]
        if "".join(str(message).split()) == "".join(str(initial_message).split()):
            raise ValidationError(_("Bitte personalisiere diesen Text"), code="invalid")
        return message
