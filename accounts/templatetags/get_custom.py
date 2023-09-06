from django.template import Library


register = Library()

@register.filter(name="get_relation")
def get_custom(dict, key):
    try:
        return dict[key].relation_type
    except:
        return None
