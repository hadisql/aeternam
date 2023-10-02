from django.template import Library

register = Library()

@register.filter(name="get_notif_name")
def get_notif_name(notif_content_object):
    return str(notif_content_object).split('|')[1][1:]
