from .models_persistent_filter import StudentListFilterModel
from .forms import form_labels
from django import forms

class StudentListFilterModelForm(forms.ModelForm):
    class Meta:
        model = StudentListFilterModel
        labels = form_labels
        labels["braucht_bezahlung"] = _("Vergütung möglich")
        exclude = []
