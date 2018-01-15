from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView

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
        print delete
        if item_id:
            item = get_object_or_404(Variation, id=item_id)
            quantity = request.GET.get('quantity', 1)
            try:
                if int(quantity) < 1:
                    delete = True
            except:  # Not very good exception catcher (this does not refelect which exception is being caught)
                raise Http404

            cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
            item_added = False
            if created:
                item_added = True
            if delete:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()

        if request.is_ajax():
            # Assuming if not deleted and not added that should reflect it is updated.
            try:
                line_item_total = cart_item.line_item_total
            except AttributeError:
                line_item_total = None

            try:
                subtotal = cart_item.cart.subtotal
            except AttributeError:
                subtotal = None

            try:
                total_items = cart_item.cart.items.count()
            except Exception:
                total_items = 0

            cart_total = cart_item.cart.total
            tax_total = cart_item.cart.tax_total
            data = {
                'item_deleted': delete,
                'item_added': item_added,
                'line_item_total': line_item_total,
                'subtotal': subtotal,
                'tax_total': tax_total,
                'cart_total': cart_total,
                'total_items': total_items
            }
            return JsonResponse(data=data)

        context = {
            'object': cart
        }
        template = self.template_name
        return render(request, template, context)


class ItemCountView(View):
    """The view to accomodate item count in the navbar """

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            cart_id = self.request.session.get('cart_id')
            if not cart_id:
                cart_item_count = 0
            else:
                cart = Cart.objects.get(id=cart_id)
                cart_item_count = cart.items.count()
                request.session['cart_item_count'] = cart_item_count
            return JsonResponse({'cart_item_count': cart_item_count})
        raise Http404


class CheckoutView(DetailView):
    model = Cart
    template_name = 'carts/checkout.html'

    def get_object(self, queryset=None):
        cart_id = self.request.session.get('cart_id', None)
        if not cart_id:
            return redirect('cart')
        cart = Cart.objects.get(id=cart_id)
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_auth = False
        if not self.request.user.is_authenticated():
            context['user_auth'] = user_auth
            context['login_form'] = AuthenticationForm()
            context['next_url'] = self.request.build_absolute_uri()
        else:
            user_auth = True
        context['user_auth'] = user_auth
        return context
