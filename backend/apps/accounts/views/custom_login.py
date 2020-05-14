import logging

from django.contrib.auth.views import LoginView

from apps.accounts.forms import CustomAuthenticationForm

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

    def post(self, request, *args, **kwargs):
        logger.info("Login Attempt (%s)", request.POST["username"])
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        logger.info("Login succesful (%s)", form.cleaned_data["username"])
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning("Login failure (%s)", getattr(form.data, "username", ""))
        return super().form_invalid(form)
