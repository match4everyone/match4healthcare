from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from .models import User, Newsletter


class HospitalSignUpForm(UserCreationForm):
    # add more query fields

    class Meta(UserCreationForm.Meta):
        model = User
        fields = []  # ['email']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_hospital = True
        user.save()
        return user


class StudentEmailForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = user.email
        user.save()
        return user


class HospitalEmailForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = user.email
        user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    # add more query fields

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        return user


from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label=_('E-Mail'),
        widget=forms.TextInput(attrs={'autofocus': True})
    )


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'message', 'send_to_hospitals', 'send_to_students', 'validation_requirement']

class NewsletterFormView(NewsletterForm):
    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].disabled = True

class TestMailForm(forms.Form):
    email = forms.EmailField()
