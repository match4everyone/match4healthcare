import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView

from apps.accounts.admin import hospital_required
from apps.ineedstudent.forms import PostingForm

logger = logging.getLogger(__name__)


@method_decorator([login_required, hospital_required], name="dispatch")
class HospitalPostingEditView(FormView):
    form_class = PostingForm
    template_name = "change_posting.html"
    success_url = "/ineedstudent/change_posting"

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.request.user.hospital, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request, messages.INFO, _("Deine Anzeige wurde erfolgreich aktualisiert."),
        )
        return super().form_valid(form)
