from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from apps.accounts.modelss import User


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
