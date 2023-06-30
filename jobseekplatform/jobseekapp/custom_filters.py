from django import template

register = template.Library()

@register.filter
def split_filter(value, delimiter):
    return value.split(delimiter)