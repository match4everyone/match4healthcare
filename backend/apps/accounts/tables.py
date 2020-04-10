import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from .models import Newsletter
from django.utils.html import format_html
from .models import NewsletterState

class NewsletterTable(tables.Table):
    sending_state = tables.Column(empty_values=(), verbose_name=_('Status'))

    class Meta:
        model = Newsletter
        fields = ['registration_date', 'subject','uuid']

    def render_uuid(self,value):
        return format_html('<a href="/accounts/view_newsletter/%s">Ansehen</a>' % value)

    def render_sending_state(self,record):
        state = record.sending_state()
        if state == NewsletterState.UNDER_APPROVAL:
            return format_html('wartet auf approvals')
        elif state == NewsletterState.SENT:
            return format_html('bereits gesendet')
        elif state == NewsletterState.READY_TO_SEND:
            return format_html('bereit zum abschicken')
        elif state == NewsletterState.BEING_EDITED:
            return format_html('wird noch editiert')
        return '--'

    def render_letterapprovedby(self,value):
        return format_html('<a href="/accounts/view_newsletter/%s">Ansehen</a>' % value)



