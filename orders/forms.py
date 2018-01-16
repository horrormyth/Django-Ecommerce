from django import forms


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    email2 = forms.EmailField(label='Verify Email')

    def validated_email(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if not email == email2:
            raise forms.ValidationError('Please make sure that provided email are same')
        return email2
