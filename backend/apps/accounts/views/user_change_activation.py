import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views.generic.base import RedirectView, View

from apps.accounts.decorator import student_required

logger = logging.getLogger(__name__)


@method_decorator([login_required, student_required], name="dispatch")
class ChangeActivationRedirect(RedirectView):
    url = "profile_student"

    def get_redirect_url(self, *args, **kwargs):
        s = self.request.user.student
        status = s.is_activated
        s.is_activated = not s.is_activated
        s.save()
        if status:
            messages.add_message(
                self.request,
                messages.INFO,
                _(
                    "Du hast dein Profil erfolgreich deaktiviert, du kannst nun keine Anfragen mehr von Hilfesuchenden bekommen."
                ),
            )
        else:
            messages.add_message(
                self.request,
                messages.INFO,
                _(
                    "Du hast dein Profil erfolgreich aktiviert, du kannst nun wieder von Hilfesuchenden kontaktiert werden."
                ),
            )
        return super().get_redirect_url(*args, **kwargs)


@method_decorator([login_required, student_required], name="dispatch")
class ChangeActivationAskView(View):
    def get(self, request):
        return render(
            request,
            "change_activation_ask.html",
            {"is_activated": request.user.student.is_activated},
        )
