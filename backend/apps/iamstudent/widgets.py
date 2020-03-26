import django.forms as forms

from django import forms
from django.forms.utils import flatatt
from django.template import loader
from django.utils.translation import ugettext_lazy

class BootstrapWidget (object):
    """
    Base class for most widgets implemented here (with the exception of :class:`TemplateWidget`).
    """

    css_classes = ('form-control',)
    """
    A tuple of CSS classes to apply to the rendered widget, in addition to any ``class`` attribute specified.
    """

    extra_attrs = {}
    """
    Extra input attributes, defined on a class level.
    """

    def build_attrs(self, *args, **kwargs):
        attrs = super(BootstrapWidget, self).build_attrs(*args, **kwargs)
        if self.is_required and not isinstance(self, RadioSelect):
            attrs.update({'aria-required': 'true'})
        if self.is_required and isinstance(self, RadioSelect):
            attrs.update({'required': 'required'})
        attrs.update(self.extra_attrs)
        new_class = '%s %s' % (attrs.get('class', ''), ' '.join(self.css_classes))
        attrs['class'] = new_class.strip()
        return attrs

class RadioSelect (BootstrapWidget, forms.RadioSelect):
    """ Bootstrap version of ``forms.RadioSelect`` """
    css_classes = ['form-check-input']
    use_fieldset = True


class MyRadioSelect(forms.NullBooleanSelect):
    input_type = 'radio'
    template_name = 'django/forms/widgets/radio.html'
    option_template_name = 'django/forms/widgets/radio_option.html'

class NullBooleanRadioSelect (RadioSelect):
    """ A ``RadioSelect`` widget for ``NullBooleanField`` """

    def __init__(self, attrs=None, unknown_label=None):
        super(NullBooleanRadioSelect, self).__init__(attrs=attrs)
        self.choices = (
            ('1', ugettext_lazy(unknown_label or 'Unknown')),
            ('2', ugettext_lazy('Yes')),
            ('3', ugettext_lazy('No'))
        )

    def render(self, name, value, attrs=None, renderer=None):
        try:
            value = {
                True: '2',
                False: '3',
                '2': '2',
                '3': '3'
            }[value]
        except KeyError:
            value = '1'
        return super(NullBooleanRadioSelect, self).render(name, value, attrs, renderer=renderer)

    def value_from_datadict(self, data, files, name):
        value = data.get(name)
        return {
            '2': True,
            True: True,
            'True': True,
            '3': False,
            'False': False,
            False: False
        }.get(value)