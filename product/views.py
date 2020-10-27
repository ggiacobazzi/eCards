from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.contrib import messages

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from cart.models import Order, OrderItem
from product.forms import NewProductForm
from product.models import Product
from shop.models import Shop
from user_management.decorators import vendor_required
import requests


@login_required
@vendor_required
def add_product_view(request):
    context = {}

    # Cache
    is_cached = ('data' in request.session)

    if not is_cached:
        response = requests.get('https://api.scryfall.com/sets')
        request.session['data'] = response.json()

    data = request.session['data']

    context['sets'] = data['data']

    return render(request, 'add_new_product.html', context)


@login_required
@vendor_required
def finalize_new_product_view(response, **kwargs):
    context = {'prod_id': kwargs.get('prod_id', False)}

    # Get Card Data
    data = requests.get('https://api.scryfall.com/cards/' + context['prod_id'])
    context['card_info'] = data.json()
    print(context['card_info'])
    if response.method == 'POST':

        new_prod_form = NewProductForm(response.POST)
        if new_prod_form.is_valid():
            obj = new_prod_form.save(commit=False)
            shop = Shop.objects.get(pk=response.user)
            obj.shop = shop
            obj.card_id = context['prod_id']

            # Get Card Image
            if 'image_uris' in context['card_info']:
                r = requests.get(context['card_info']['image_uris']['small'])
            else:
                r = requests.get(context['card_info']['card_faces'][0]['image_uris']['small'])

            img_temp = NamedTemporaryFile()
            img_temp.write(r.content)
            img_temp.flush()

            obj.image.save("image.png", File(img_temp), save=True)
            obj.title = context['card_info']['name']
            obj.save()

            return redirect('shop:my_shop')

        else:
            context['new_prod_form'] = new_prod_form
    else:
        context['new_prod_form'] = NewProductForm()

    return render(response, 'finalize_new_product.html', context)


class ProductChange(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'edit_product.html'
    form_class = NewProductForm
    success_url = reverse_lazy('shop:my_shop')


@login_required
@vendor_required
def remove_product_view(response):
    prod_id = response.POST.get('prodid')
    success = True
    try:
        product_delete = Product.objects.filter(id=prod_id)
        product_delete.delete()
        messages.success(response, 'Product removed successfully', extra_tags='alert-success '
                                                                              'alert-dismissible')
    except Product.DoesNotExist:
        success = False
        messages.error(response, 'Product not removed',
                       extra_tags='alert-danger alert-dismissible')

    return JsonResponse({"state": success})


@login_required
@vendor_required
def send_product_view(response):
    data = {'success': False}

    order_id = response.POST.get('sale_id')
    print(order_id)
    order = OrderItem.objects.get(pk=order_id)
    if order:
        order.is_sent = True
        order.save()
        data['success'] = True
        messages.info(response, 'Product sent', extra_tags='alert-success alert-dismissible')

    return JsonResponse(data)
