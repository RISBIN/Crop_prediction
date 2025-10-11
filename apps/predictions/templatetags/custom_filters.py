"""
Custom template filters for predictions app
"""
from django import template

register = template.Library()


@register.filter(name='mul')
def multiply(value, arg):
    """Multiply the arg with the value"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0
