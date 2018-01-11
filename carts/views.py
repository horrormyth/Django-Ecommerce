from django.shortcuts import get_object_or_404, render
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from carts.models import CartItem, Cart
from products.models import Variation


class CartView(SingleObjectMixin, View):
    model = Cart
    template_name = 'carts/view.html'

    def get_object(self, *args, **kwargs):
        self.request.session.set_expiry(0)  # until the browser closes
        cart_id = self.request.session.get('cart_id', None)
        if not cart_id:
            # Create cart
            cart = Cart()
            cart.save()
            cart_id = cart.id
            self.request.session['cart_id'] = cart_id

        cart = Cart.objects.get(id=cart_id)
        if self.request.user.is_authenticated():
            cart.user = self.request.user
            cart.save()
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_object()
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

        context = {
            'object': cart
        }
        template = self.template_name
        return render(request, template, context)
