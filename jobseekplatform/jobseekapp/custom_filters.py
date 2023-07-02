from django import template
import os

register = template.Library()


@register.filter
def split_filter(value, delimiter):
    return value.split(delimiter)


@register.filter
def get_filename(value):
    return os.path.basename(value)
