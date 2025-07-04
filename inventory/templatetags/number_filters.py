from django import template

register = template.Library()

@register.filter
def comma_miles(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except:
        return value

@register.filter
def mul(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return ''