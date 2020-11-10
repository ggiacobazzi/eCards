from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect

from cart.models import Order, OrderItem
from shop.models import Shop
from .decorators import admin_required, user_required
from .forms import RegisterFormNormalUser, RegisterFormVendor, LoginForm

# Create your views here.
from .models import CustomUser

import _datetime


def register(response):
    if response.method == 'POST':
        form = RegisterFormNormalUser(response.POST)
        if form.is_valid():
            user = form.save()

            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # account = authenticate(username=username, password=raw_password)
            login(response, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/home')

    else:
        form = RegisterFormNormalUser()

    return render(response, 'registration.html', {"form": form})


def register_vendor(response):
    if response.method == 'POST':
        form = RegisterFormVendor(response.POST)
        if form.is_valid():
            user = form.save()
            login(response, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/home')
    else:
        form = RegisterFormVendor()

    return render(response, 'registration_vendor.html', {"formVendor": form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully', extra_tags='alert-success alert-dismissible')
    return redirect('home')


def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            # username = request.POST['username']
            # password = request.POST['password']
            user = form.save()

            if user is not None:
                if user.is_active:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    messages.success(request, 'Logged in successfully', extra_tags='alert-success alert-dismissible')
                    return redirect('/home')
                else:
                    context['error'] = "Non active User"
            else:
                context['error'] = "User is None"

    else:
        form = LoginForm()

    context['login_form'] = form
    return render(request, 'login.html', context)


@user_required
def account_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('user_management:login')
    context = {}
    users = CustomUser.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    orders = Order.objects.filter(user=request.user.id)
    context['users'] = users
    context['orders'] = orders
    user = CustomUser.objects.get(username=request.user.username)
    if user.is_vendor:
        shop = Shop.objects.get(pk=user)
        orders = OrderItem.objects.filter(shop=shop)
        # month = get_current_month()
        # year = get_current_year()
        # orders_month = OrderItem.objects.filter(date_added__month=month, date_added__year=year)
        #
        # total_earnings_mth = 0
        # total_sent_mth = 0

        total_earnings = 0
        total_sent = 0
        for order in orders:
            total_earnings += order.final_price
            if order.is_sent:
                total_sent += 1

        # for order in orders_month:
        #     total_earnings_mth += order.final_price
        #     if order.is_sent:
        #         total_sent_mth += 1
        #
        # context['sales_mth'] = orders_month
        # context['total_earnings_mth'] = total_earnings_mth
        # context['total_sent_mth'] = total_sent_mth

        context['sales'] = orders
        context['total_earnings'] = total_earnings
        context['total_sent'] = total_sent

    return render(request, 'account_profile.html', context)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required
def close_account(request):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(username=request.user.username)
            user.is_active = False
            user.save()
            logout(request)
            messages.success(request, 'Profile successfully disabled', extra_tags='alert-success alert-dismissible')
            return redirect('home')
        except User.DoesNotExist:
            messages.error(request, ' Profile does not exist', extra_tags='alert-danger alert-dismissible')
            return redirect('home')
    return render(request, 'close_account.html')


@admin_required
def ban_user_view(request):
    data = {'success': False}
    usr = request.POST.get('username')
    user = CustomUser.objects.get(username=usr)
    if user:
        if request.method == 'POST':
            user.is_active = False
            user.save()
            messages.success(request, 'User ' + usr + ' banned successfully', extra_tags='alert-success '
                                                                                         'alert-dismissible')
            data['success'] = True
    else:
        messages.error(request, 'User ' + usr + ' doesn\'t exist',
                       extra_tags='alert-danger alert-dismissible')

    return JsonResponse(data)


@admin_required
def unban_user_view(request):
    data = {'success': False}
    usr = request.POST.get('username')
    user = CustomUser.objects.get(username=usr)
    if user:
        if request.method == 'POST':
            user.is_active = True
            user.save()
            messages.success(request, 'User ' + usr + ' unbanned successfully', extra_tags='alert-success '
                                                                                           'alert-dismissible fade show')
            data['success'] = True
    else:
        messages.error(request, 'User ' + usr + ' doesn\'t exist',
                       extra_tags='alert-danger alert-dismissible fade show')

    return JsonResponse(data)


@user_required
def get_orders_view(request):
    data = {'success': False}

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(pk=order_id)
        prod_data = serializers.serialize('json', order.get_cart_items())
        return JsonResponse(prod_data, safe=False)

    return JsonResponse(data)

#
# def get_current_month():
#     now = datetime.now()
#     return now.strftime("%m")
#
#
# def get_current_year():
#     now = datetime.now()
#     return now.strftime("%y")