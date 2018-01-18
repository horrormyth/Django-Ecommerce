from django.views.generic import FormView

from .forms import AddressForm


class AddressSelectFormView(FormView):
    form_class = AddressForm
    template_name = 'orders/address_select.html'
