from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

# Create your views here.
from cart.forms import PaymentForm
from cart.models import Order, OrderItem
from product.models import Product
from shop.models import Shop
from user_management.models import CustomUser
import datetime


def get_user_pending_order(request):
    user = CustomUser.objects.get(username=request.user.username)
    order = Order.objects.filter(user=user, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required
def add_to_cart_view(request):
    data = {'success': False}

    user = CustomUser.objects.get(username=request.user.username)
    shop = Shop.objects.get(name=request.POST.get('shop'))
    quantity = request.POST.get('quantity')
    product = Product.objects.get(pk=request.POST.get('prod_id'))

    product.quantity -= int(quantity)
    product.save()
    order_item = OrderItem.objects.create(product=product)
    order_item.final_price = request.POST.get('total')
    order_item.shop = shop
    order_item.quantity = quantity
    order_item.save()

    user_order, status = Order.objects.get_or_create(user=user, is_ordered=False)

    user_order.items.add(order_item)

    messages.info(request, "Item added to cart", extra_tags='alert-success alert-dismissible')
    data['success'] = True

    return JsonResponse(data)


@login_required
def delete_from_cart_view(request):
    data = {'success': False}
    item_id = request.POST.get('product')
    item_to_delete = OrderItem.objects.get(pk=item_id)
    if item_to_delete is not None:
        item_to_delete.product.quantity += int(item_to_delete.quantity)
        item_to_delete.product.save()
        item_to_delete.delete()
        messages.info(request, "Item has been deleted", extra_tags='alert-success alert-dismissible')

    data['success'] = True

    return JsonResponse(data)


@login_required
def cart_summary_view(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {'order': existing_order}
    return render(request, 'cart_summary.html', context)


@login_required
def checkout_view(request):
    order = get_user_pending_order(request)
    context = {'order': order}

    if request.method == 'POST':
        payment_form = PaymentForm(request.POST or None)
        if payment_form.is_valid():
            order_to_purchase = Order.objects.get(pk=order.id, is_ordered=False)
            order_to_purchase.shipping_address = payment_form.cleaned_data.get('shipping_address')
            order_to_purchase.shipping_country = payment_form.cleaned_data.get('shipping_country')
            order_to_purchase.credit_card_number = payment_form.cleaned_data.get('credit_card_number')
            order_to_purchase.cvv = payment_form.cleaned_data.get('cvv')
            order_to_purchase.is_ordered = True
            order_to_purchase.date_ordered = datetime.datetime.now()
            order_to_purchase.save()

            order_items = order_to_purchase.items.all()
            order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
            messages.info(request, "Thank you! Your purchase was successful!", extra_tags='alert-success '
                                                                                          'alert-dismissible')
            return redirect('user_management:profile')
        else:
            context['payment_form'] = payment_form
    else:
        context['payment_form'] = PaymentForm()
    return render(request, 'checkout.html', context)
