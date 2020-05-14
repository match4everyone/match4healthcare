from django import forms


class TestMailForm(forms.Form):
    email = forms.EmailField()
