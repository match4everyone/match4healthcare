import logging

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import RedirectView

from apps.accounts.modelss import Newsletter

logger = logging.getLogger(__name__)


@method_decorator([login_required, staff_member_required], name="dispatch")
class NewNewsletterRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        newsletter = Newsletter.objects.create()
        newsletter.letter_authored_by.add(self.request.user)
        newsletter.save()
        self.url = "view_newsletter/" + str(newsletter.uuid)
        return super().get_redirect_url(*args, **kwargs)
