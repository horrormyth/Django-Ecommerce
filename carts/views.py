from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from carts.models import CartItem, Cart
from products.models import Variation


class CartView(View):
    def get(self, request, *args, **kwargs):
        request.session.set_expiry(0)  # until the browser closes
        cart_id = request.session.get('cart_id', None)
        if not cart_id:
            # Create cart
            cart = Cart()
            cart.save()
            cart_id = cart.id
            request.session['cart_id'] = cart_id

        cart = Cart.objects.get(id=cart_id)
        if request.user.is_authenticated():
            cart.user = request.user
            cart.save()
        item_id = request.GET.get('item', None)
        delete = request.GET.get('delete', False)
        if item_id:
            item = get_object_or_404(Variation, id=item_id)
            quantity = request.GET.get('quantity', 1)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
            if delete:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
        return HttpResponseRedirect('/')
