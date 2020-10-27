from django import forms

from product.models import Product


class NewProductForm(forms.ModelForm):
    price = forms.DecimalField(required=True, max_digits=10, decimal_places=2, min_value=0.1)
    quantity = forms.IntegerField(min_value=0)
    shipment = forms.DecimalField(required=True, max_digits=10, decimal_places=2, min_value=0)

    class Meta:
        model = Product
        fields = ("price", "quantity", "shipment")

