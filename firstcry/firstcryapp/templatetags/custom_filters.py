from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg


@register.filter
def get_attribute(obj, attr_name):
    return getattr(obj, attr_name, None)

@register.filter
def absolute(value):
    return abs(value)

@register.filter
def with_index(items, start=1):
    return zip(range(start, start + len(items)), items)