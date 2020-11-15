from django import template

register = template.Library()


@register.simple_tag
def model_name(value):
    if hasattr(value, 'model'):
        value = value.model

    return value._meta.model_name
