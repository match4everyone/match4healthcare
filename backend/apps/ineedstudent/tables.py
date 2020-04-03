import django_tables2 as tables
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


class ContactedTable(tables.Table):
    registration_date = tables.Column(verbose_name=_('E-Mail versendet am'))
    is_activated = tables.Column(empty_values=(), verbose_name=_('Helfer*in noch verfügbar'))
    details = tables.TemplateColumn(template_name='modal_button.html', verbose_name=_(''))

    # todo add link to student detail view to button
    # student_info = tables.TemplateColumn(template_name='student_info_button.html',verbose_name=_(''))

    def render_is_activated(self, value):
        if value:
            return format_html(_('<div class="text-center">ja</div>'))
        return format_html(_('<div class="text-center">nein</div>'))
