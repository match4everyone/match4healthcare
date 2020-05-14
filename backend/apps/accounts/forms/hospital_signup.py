from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from apps.accounts.modelss import User


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
