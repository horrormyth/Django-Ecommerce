from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import FormView

from .forms import AddressForm
from .models import UserAddress, UserCheckout


class AddressSelectFormView(FormView):
    form_class = AddressForm
    template_name = 'orders/address_select.html'

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
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

        if not (bill_address and ship_address):
            # create a view to add the address
            redirect('')

        form.fields['billing_address'].queryset = bill_address
        form.fields['shipping_address'].queryset = ship_address

        return form

    def form_valid(self, form, *args, **kwargs):
        billing_address = form.cleaned_data.get('billing_address')
        shipping_address = form.cleaned_data.get('shipping_address')
        self.request.session['billing_address_id'] = billing_address.id
        self.request.session['shipping_address_id'] = shipping_address.id
        return super(AddressSelectFormView, self).form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse('checkout')
