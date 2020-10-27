from django import forms

from cart.models import Order


class PaymentForm(forms.ModelForm):
    shipping_address = forms.CharField(max_length=100)
    shipping_country = forms.CharField(max_length=60)
    credit_card_number = forms.IntegerField()
    cvv = forms.IntegerField(max_value=999)

    class Meta:
        model = Order
        fields = ('shipping_address', 'shipping_country', 'credit_card_number', 'cvv')
