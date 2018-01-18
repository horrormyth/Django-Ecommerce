from django.core.urlresolvers import reverse
from django.views.generic import FormView

from .models import UserAddress
from .forms import AddressForm


class AddressSelectFormView(FormView):
    form_class = AddressForm
    template_name = 'orders/address_select.html'

    def get_form(self, *args, **kwargs):
        form = super(AddressSelectFormView, self).get_form(*args, **kwargs)
        form.fields['billing_address'].queryset = UserAddress.objects.filter(
            user__email=self.request.user.email,
            address_type='billing',
        )
        form.fields['shipping_address'].queryset = UserAddress.objects.filter(
            user__email=self.request.user.email,
            address_type='shipping',
        )

        return form

    def get_success_url(self, *args, **kwargs):
        return reverse('checkout')
