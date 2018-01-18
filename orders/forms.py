from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    email2 = forms.EmailField(label='Verify Email')

    def clean_email2(self):
        """ Validating email, especially field email2"""
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email == email2:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('User already exists!! Please login instead. ')
            return email2
        else:
            raise forms.ValidationError('Please make sure provided email are same')


class AddressForm(forms.Form):
    billing_address = forms.CharField()
    shipping_address = forms.CharField()
