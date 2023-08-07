from django import template

register = template.Library()

@register.filter
def list_item(lst, i):
    try:
        return lst[i]
    except:
        return None

#https://stackoverflow.com/questions/53287022/django-template-access-to-list-item-by-forloop-counter
