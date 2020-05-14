from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(label=_("E-Mail"), widget=forms.TextInput(attrs={"autofocus": True}))
