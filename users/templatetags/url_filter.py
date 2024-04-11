from django import template

register = template.Library()

@register.filter
def split_url(value, separator):
    return value.split(separator)