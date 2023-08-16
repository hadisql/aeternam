from django.template import Library


register = Library()

@register.filter(name="get_relation")
def get_custom(dict, key):
    return dict[key].relation_type
