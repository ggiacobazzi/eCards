from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from product.forms import NewProductForm
from product.models import Product
from shop.forms import MyShopForm
from shop.models import Shop, Review
from user_management.decorators import user_required, vendor_required
from user_management.models import CustomUser


@user_required
def create_shop_view(request):
    context = {}

    if request.POST:
        user = request.user
        form = MyShopForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            user.is_vendor = True
            user.has_shop = True
            user.save()
            form.save()

            return redirect('shop:my_shop')
        else:
            context['form'] = form
    else:
        form = MyShopForm()
        context['form'] = form

    return render(request, 'create_new_shop.html', context)


@user_required
def create_shop_view_partial(request):
    context = {}

    if request.POST:
        user = request.user
        form = MyShopForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            user.is_vendor = True
            user.has_shop = True
            user.save()
            form.save()

            return redirect('shop:my_shop')
        else:
            context['form_partial'] = form
    else:
        form = MyShopForm()
        context['form'] = form

    return render(request, 'create_new_shop_partial.html', context)


@vendor_required
def my_shop_view(request):
    context = {}

    try:
        shop = Shop.objects.get(pk=request.user)

        # Get Products
        products = Product.objects.filter(shop=shop)
        # Get Reviews
        reviews = Review.objects.filter(shop=shop)

    except Shop.DoesNotExist:
        shop = None
    context['shop'] = shop
    context['products'] = products
    context['reviews'] = reviews
    context['form'] = NewProductForm()
    return render(request, 'my_shop.html', context)


def shop_detail_view(request, name):
    context = {}

    try:
        shop = Shop.objects.get(name=name)
        products = Product.objects.filter(shop=shop)
        reviews = Review.objects.filter(shop=shop)

        rating = []
        if reviews.__len__() > 0:
            for r in reviews:
                rating.append(r.rating)
                context['general_rating'] = round((sum(rating) / len(rating)), 1)
        else:
            context['general_rating'] = 0
        context['products'] = products
        context['reviews'] = reviews
    except Shop.DoesNotExist:
        shop = None
    context['shop'] = shop
    context['vendor'] = shop.user

    return render(request, 'shop_detail.html', context)


@user_required
def shop_add_review_view(request):
    data = {'success': False}
    if request.method == 'POST':
        review = Review()
        shop = Shop.objects.get(name=request.POST.get('shop'))
        if shop is not None:
            review.shop = shop
        review.review = request.POST.get('review')
        review.rating = request.POST.get('rating')

        # Error Rating
        if int(review.rating) < 0 or int(review.rating) > 5:
            data['success'] = False
            response = JsonResponse(data)
            response.status_code = 403
            return response

        user = CustomUser.objects.get(id=request.POST.get('user'))
        if user is not None:
            review.account = user
        review.save()
        data['success'] = True
    return JsonResponse(data)
