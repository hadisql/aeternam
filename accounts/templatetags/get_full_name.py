from django.template import Library


register = Library()

@register.filter(name="get_full_name")
def get_full_name(user):
    try:
        return user.get_full_name() or user.email
    except:
        return None
