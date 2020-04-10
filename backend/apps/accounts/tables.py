import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from .models import Newsletter
from django.utils.html import format_html
from .models import NewsletterState

NewsletterStateIcons = {
    NewsletterState.READY_TO_SEND: '<svg class="bi bi-file-check" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path d="M9 1H4a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V8h-1v5a1 1 0 01-1 1H4a1 1 0 01-1-1V3a1 1 0 011-1h5V1z"/> <path fill-rule="evenodd" d="M15.854 2.146a.5.5 0 010 .708l-3 3a.5.5 0 01-.708 0l-1.5-1.5a.5.5 0 01.708-.708L12.5 4.793l2.646-2.647a.5.5 0 01.708 0z" clip-rule="evenodd"/></svg>',
    NewsletterState.UNDER_APPROVAL: '<svg class="bi bi-exclamation-triangle" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M7.938 2.016a.146.146 0 00-.054.057L1.027 13.74a.176.176 0 00-.002.183c.016.03.037.05.054.06.015.01.034.017.066.017h13.713a.12.12 0 00.066-.017.163.163 0 00.055-.06.176.176 0 00-.003-.183L8.12 2.073a.146.146 0 00-.054-.057A.13.13 0 008.002 2a.13.13 0 00-.064.016zm1.044-.45a1.13 1.13 0 00-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566z" clip-rule="evenodd"/><path d="M7.002 12a1 1 0 112 0 1 1 0 01-2 0zM7.1 5.995a.905.905 0 111.8 0l-.35 3.507a.552.552 0 01-1.1 0L7.1 5.995z"/></svg>',
    NewsletterState.SENT: '<svg class="bi bi-check" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M13.854 3.646a.5.5 0 010 .708l-7 7a.5.5 0 01-.708 0l-3.5-3.5a.5.5 0 11.708-.708L6.5 10.293l6.646-6.647a.5.5 0 01.708 0z" clip-rule="evenodd"/></svg>',
    NewsletterState.BEING_EDITED: '<svg class="bi bi-pencil" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M11.293 1.293a1 1 0 011.414 0l2 2a1 1 0 010 1.414l-9 9a1 1 0 01-.39.242l-3 1a1 1 0 01-1.266-1.265l1-3a1 1 0 01.242-.391l9-9zM12 2l2 2-9 9-3 1 1-3 9-9z" clip-rule="evenodd"/><path fill-rule="evenodd" d="M12.146 6.354l-2.5-2.5.708-.708 2.5 2.5-.707.708zM3 10v.5a.5.5 0 00.5.5H4v.5a.5.5 0 00.5.5H5v.5a.5.5 0 00.5.5H6v-1.5a.5.5 0 00-.5-.5H5v-.5a.5.5 0 00-.5-.5H3z" clip-rule="evenodd"/></svg>',
}


class NewsletterTable(tables.Table):
    sending_state = tables.Column(empty_values=(), verbose_name=_('Status'),attrs={'th':{'style':"width: 16.66%"}})

    class Meta:
        model = Newsletter
        fields = ['registration_date', 'subject', 'uuid']
        sequence = ('registration_date', 'subject', 'sending_state', 'uuid')
        template_name = "django_tables2/bootstrap4.html"
        attrs = {
            'data-toggle': "table",
            'data-search': "false",
            'data-filter-control': "true",
            'data-show-export': "false",
            'data-click-to-select': "false",
            'data-toolbar': "#toolbar",
            'class': "table"
        }

    def render_uuid(self, value):
        return format_html('<a href="/accounts/view_newsletter/%s">Details</a>' % value)

    def render_sending_state(self, record):
        state = record.sending_state()

        if state == NewsletterState.UNDER_APPROVAL:
            text = 'wartet auf approvals'
        elif state == NewsletterState.SENT:
            text = 'bereits gesendet'
        elif state == NewsletterState.READY_TO_SEND:
            text = 'bereit zum abschicken'
        elif state == NewsletterState.BEING_EDITED:
            text = 'wird noch editiert'
        else:
            return '--'

        icon = NewsletterStateIcons[state]
        return format_html(icon + ' ' + text)

    def render_letterapprovedby(self, value):
        return format_html('<a href="/accounts/view_newsletter/%s">Ansehen</a>' % value)
