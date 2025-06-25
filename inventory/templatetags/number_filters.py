from django import template

register = template.Library()

@register.filter
def comma_miles(value):
    try:
        return f"{int(value):,}".replace(",", ".")
    except:
        return value