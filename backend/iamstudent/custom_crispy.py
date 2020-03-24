from crispy_forms.bootstrap import Field
from crispy_forms.utils import TEMPLATE_PACK

class InputButtonGroup(Field):
    """
    Layout object for rendering radio and checkbox elements as button groups::

        RadioButtons('field_name', [option_label_class="btn blue text-white btn-lg"])
    """
    template = "%s/layout/input_buttongroup.html"

    def __init__(self, *args, **kwargs):

        try:
            self.input_type
        except AttributeError:
            raise NotImplementedError(
                'Cannot instantiate {}.  input_type property must be set'.format(
                    type(self).__name__))

        self.option_label_class = 'btn btn-secondary'
        if 'option_label_class' in kwargs:
            self.option_label_class = kwargs.pop('option_label_class')
        return super(InputButtonGroup, self).__init__(*args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return super(InputButtonGroup, self).render(
            form, form_style, context, template_pack=template_pack,
            extra_context={
                'input_type': self.input_type,
                'option_label_class': self.option_label_class
            }
        )

class RadioButtons(InputButtonGroup):
    input_type = 'radio'

class CheckboxButtons(InputButtonGroup):
    input_type = 'checkbox'
