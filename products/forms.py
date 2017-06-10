from django import forms
from .models import Variation

from django.forms.models import modelformset_factory

"""Form for editing inventory"""

class VariationInventoryForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = [
            'title',
            'price',
            'sale_price',
            'inventory',
            'active'
        ]

VariationInventoryFormSet = modelformset_factory(Variation, form = VariationInventoryForm, extra = 1)