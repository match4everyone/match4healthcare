from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from . import models


class StudentEvaluationForm(UserPassesTestMixin, CreateView):

    def test_func(self):
        return self.request.user.is_student and not self.request.user.has_evaluated

    model = models.StudentEvaluation
    fields = '__all__'
