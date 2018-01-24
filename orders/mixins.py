from django.shortcuts import redirect

from carts.models import Cart
from models import Order


class CartOrderMixin(object):

    def get_order(self, *args, **kwargs):
        cart = self.get_cart()
        new_order_id = self.request.session.get('order_id', None)
        if not new_order_id:
            new_order = Order.objects.create(cart=cart)
            self.request.session['order_id'] = new_order.id
        else:
            new_order = Order.objects.get(id=new_order_id)

        return new_order

    def get_cart(self, *args, **kwargs):
        cart_id = self.request.session.get('cart_id', None)
        if not cart_id:
            return redirect('cart')
        cart = Cart.objects.get(id=cart_id)
        return cart
