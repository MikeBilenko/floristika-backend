from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_api_path():
    return f"{settings.BASE_URL_PATH}/api/v1/"
