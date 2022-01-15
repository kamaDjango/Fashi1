from django import template
from mainApp.models import Product
register = template.Library()

@register.filter(name='quantity')
def quantity(request,pid):
    cart = request.session.get("cart",None)
    if(cart):
        for i in cart.keys():
            if(i==str(pid)):
                return cart[str(pid)]
    return 0

@register.filter(name='finalPrice')
def finalPrice(request,pid):
    cart = request.session.get("cart",None)
    p = Product.objects.get(pid=int(pid))
    if(cart):
        for i in cart.keys():
            if(i==str(pid)):
                return cart[str(pid)]*p.finalPrice
    return 0