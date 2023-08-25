from django.template import Library


register = Library()

@register.filter(name="is_notif")
def is_notif(dict):
    # checks if there is any notification in the categorized_notifications dictionary
    is_notif = False
    for _, v in dict.items():
        is_notif = len(v)
        if is_notif:
            break
    return is_notif
