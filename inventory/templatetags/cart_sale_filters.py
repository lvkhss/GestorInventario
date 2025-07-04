from django import template

register = template.Library()

@register.filter
def get_cart_sale_total(sale):
    return sum(item.quantity * item.price_at_sale for item in sale.items.all())
