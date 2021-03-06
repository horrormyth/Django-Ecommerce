import braintree
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

from carts.models import CartItem, Cart
from orders.forms import GuestCheckoutForm
from orders.mixins import CartOrderMixin
from orders.models import UserCheckout
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


class CheckoutView(CartOrderMixin, FormMixin, DetailView):
    model = Cart
    template_name = 'carts/checkout.html'
    form_class = GuestCheckoutForm

    def get_object(self, *args, **kwargs):
        cart = self.get_cart()
        return cart

    def get_context_data(self, *args, **kwargs):
        context = super(CheckoutView, self).get_context_data(*args, **kwargs)
        user_auth = False
        user = self.request.user
        user_checkout_id = self.request.session.get('user_checkout_id', None)
        if user.is_authenticated():
            user_checkout, created = UserCheckout.objects.get_or_create(email=user.email)
            user_checkout.user = user
            user_checkout.save()
            context['bt_client_token'] = user_checkout.get_braintree_client_token()
            user_auth = True
            self.request.session['user_checkout_id'] = user_checkout.id
        elif not self.request.user.is_authenticated() and not user_checkout_id:
            context['login_form'] = AuthenticationForm
            context['next_url'] = self.request.build_absolute_uri()
        elif user_checkout_id:
            user_auth = True
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            context['bt_client_token'] = user_checkout.get_braintree_client_token()
        else:
            pass
        context['order'] = self.get_order()
        context['user_auth'] = user_auth
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user_checkout, created = UserCheckout.objects.get_or_create(email=email)
            request.session['user_checkout_id'] = user_checkout.id
            return self.form_valid(form=form)
        else:
            return self.form_invalid(form=form)

    def get_success_url(self):
        return reverse('checkout')

    def get(self, request, *args, **kwargs):
        get_data = super(CheckoutView, self).get(request, *args, **kwargs)
        cart = self.get_object()
        if not cart:
            return redirect('cart')
        new_order = self.get_order()
        user_checkout_id = request.session.get('user_checkout_id')
        if user_checkout_id:
            user_checkout = UserCheckout.objects.get(id=user_checkout_id)
            if not (new_order.billing_address and new_order.shipping_address):
                return redirect('order_address')
            new_order.user = user_checkout
            new_order.save()
        return get_data


class FinalCheckoutView(CartOrderMixin, View):

    def post(self, request, *args, **kwargs):
        order = self.get_order()
        order_total = order.order_total
        payment_nonce = request.POST.get('payment_method_nonce', None)
        if payment_nonce:
            result = braintree.Transaction.sale({
                "amount": order_total,
                "payment_method_nonce": payment_nonce,
                # Todo add more fields such as billing/shipping address, names,etc
                "options": {
                    "submit_for_settlement": True
                }
            })

            if result.is_success:
                order.mark_completed(transaction_id=result.transaction.id)
                messages.success(request, 'Thank you for the order')
                del request.session['cart_id']
                del request.session['order_id']
            else:
                messages.success(request, '{}'.format(result.message))
                return redirect('checkout')
        return redirect('order_detail', pk=order.pk)

    def get(self, request, *args, **kwargs):
        return redirect('checkout')
