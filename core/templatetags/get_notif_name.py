from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter(name="get_notif_name")
def get_notif_name(notif_content_object):
    return str(notif_content_object).split('|')[1][1:]

@register.filter
@stringfilter
def up_to(value, delimiter=None):
    return value.split(delimiter)[0]
up_to.is_safe = True
