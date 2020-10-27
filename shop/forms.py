from django import forms

from shop.models import Shop, Review


class MyShopFormUser(forms.ModelForm):
    name = forms.CharField(max_length=30, help_text='Choose a name for your shop')
    description = forms.Textarea()
    address = forms.CharField(max_length=30)
    telephone = forms.CharField(max_length=15)
    photo = forms.ImageField(required=False)

    class Meta:
        model = Shop
        fields = ("name", "description", "address", "telephone", "photo")


class MyShopForm(forms.ModelForm):
    name = forms.CharField(max_length=30, help_text='Choose a name for your shop')
    description = forms.Textarea()
    photo = forms.ImageField(required=False)

    class Meta:
        model = Shop
        fields = ("name", "description", "photo")


# class NewReviewForm(forms.ModelForm):
#     rating = forms.IntegerField(required=True, min_value=1, max_value=5)
#     review = forms.Textarea()
#
#     class Meta:
#         model = Review
#         fields = {"rating", "review"}
