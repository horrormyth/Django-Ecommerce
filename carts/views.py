from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
# Create your views here.
from carts.models import CartItem, Cart
from products.models import Variation


class CartView(View):

    def get(self, request, *args, **kwargs):
        item_id = request.GET.get('item', None)
        delete = request.GET.get('delete', False)
        if item_id:
            item_instance = get_object_or_404(Variation, id=item_id)
            quantity = request.GET.get('quantity', 1)
            cart = Cart.objects.last()
            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
            if delete:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
        return HttpResponseRedirect('/')
