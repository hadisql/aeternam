#this should be at the top of your custom template tags file
from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()

@register.filter
@stringfilter
def up_to(value, delimiter=None):
    return value.split(delimiter)[0]
up_to.is_safe = True
