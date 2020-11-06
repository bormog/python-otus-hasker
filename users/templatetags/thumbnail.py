from django import template
import os

register = template.Library()


@register.simple_tag
def thumbnail_url(value):
    file, ext = os.path.splitext(value.url)
    return '%s.thumbnail%s' % (file, ext)
