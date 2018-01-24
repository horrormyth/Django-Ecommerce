from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import FormView, CreateView

from mixins import CartOrderMixin
from .forms import AddressForm, UserAddressForm
from .models import UserAddress, UserCheckout


class UserAddressCreateView(CreateView):
    form_class = UserAddressForm
    template_name = 'forms.html'
    success_url = '/checkout/address/'

    def get_checkout_user(self):
        user_checkout_id = self.request.session.get('user_checkout_id')
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        return user_checkout

    def form_valid(self, form, *args, **kwargs):
        form.instance.user = self.get_checkout_user()
        return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)


class AddressSelectFormView(CartOrderMixin, FormView):
    form_class = AddressForm
    template_name = 'orders/address_select.html'

    def dispatch(self, *args, **kwargs):
        billin_address, shipping_address = self.get_address()
        if not billin_address:
            messages.success(self.request, 'Please add billing address to continue')
            return redirect('create_address')
        elif not shipping_address:
            messages.success(self.request, 'Please add shipping address to continue')
            return redirect('create_address')
        else:
            return super(AddressSelectFormView, self).dispatch(*args, **kwargs)

    def get_address(self, *args, **kwargs):
        user_checkout_id = self.request.session.get('user_checkout_id', None)
        user_checkout = UserCheckout.objects.get(id=user_checkout_id)
        bill_address = UserAddress.objects.filter(
            user=user_checkout,
            address_type='billing',
        )
        ship_address = UserAddress.objects.filter(
            user=user_checkout,
            address_type='shipping',
        )
        return bill_address, ship_address

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        bill_address, ship_address = self.get_address()
        form.fields['billing_address'].queryset = bill_address
        form.fields['shipping_address'].queryset = ship_address
        return form

    def form_valid(self, form, *args, **kwargs):
        billing_address = form.cleaned_data.get('billing_address')
        shipping_address = form.cleaned_data.get('shipping_address')
        order = self.get_order()
        order.billing_address = billing_address
        order.shipping_address = shipping_address
        order.save()
        return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('checkout')
