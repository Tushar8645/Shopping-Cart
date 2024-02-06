from django import template

register = template.Library()


@register.filter(name='isCart')
def isCart(product, cart):
    keys = cart.keys()

    for id in keys:
        if int(id) == product.pk:
            return True

    return False


@register.filter(name='cartQuantity')
def cartQuantity(product, cart):
    keys = cart.keys()

    for id in keys:
        if int(id) == product.pk:
            return cart.get(id)


@register.filter(name='priceTotal')
def priceTotal(product, cart):
    return product.price * cartQuantity(product, cart)


@register.filter(name='totalCartPrice')
def totalCartPrice(products, cart):
    sum = 0

    for p in products:
        sum += priceTotal(p, cart)

    return sum
