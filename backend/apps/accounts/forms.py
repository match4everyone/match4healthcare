from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout,Field, Row, Column, Div, HTML, Button
from crispy_forms.bootstrap import InlineRadios, PrependedText

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


class BaseNewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['subject', 'message', 'send_to_hospitals', 'send_to_students', 'validation_requirement']
        labels = {
            'send_to_hospitals': _('Institutionen'),
            'send_to_students': _('Helfer*innen'),
            'message': _('Nachricht'),
            'validation_requirement': _('Davon nur an ... Benutzer')
        }

    def __init__(self, *args, **kwargs):
        super(BaseNewsletterForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if f in ['message','subject']:
                self.fields[f].label = False
        self.helper = FormHelper()
        self.helper.form_style = 'inline'
        self.helper.form_class = 'form-inline'

        self.helper.layout = Layout(
                                    Row(Column(HTML('<h5>Adressaten</h5>')),Column(Row(HTML('Dieser Newsletter geht an')),
                                        Row('send_to_students'),
                                        Row('send_to_hospitals')),
                                        Column('validation_requirement')),
                                    HTML('<hr>'),
                                    PrependedText('subject', '[match4healthcare]', placeholder="Betreff"),
                                    'message')

class NewsletterForm(BaseNewsletterForm):
    def __init__(self, *args,uuid=None, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = '/accounts/view_newsletter/' + str(uuid)

        self.helper.attrs = {
            'onsubmit': 'disableButton()'
        }
        self.helper.add_input(Submit('submit', 'Änderungen Speichern',css_class='btn-success'))


class NewsletterFormView(BaseNewsletterForm):
    def __init__(self, *args, **kwargs):
        super(NewsletterFormView, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].disabled = True
            self.fields[f].required = False
        self.helper.form_tag = False

class TestMailForm(forms.Form):
    email = forms.EmailField()
