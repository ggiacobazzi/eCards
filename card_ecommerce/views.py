from django.http import HttpResponse
from django.shortcuts import render

from product.models import Product


def test_view(request):
    return HttpResponse("View di prova con HttpResponse")


def base(request):
    return render(request, 'base.html')


def home(request):
    context = {}

    new_products = Product.objects.all().order_by('date')
    context['new_products'] = new_products

    return render(request, 'home.html', context)


def forbidden_view(request):
    return render(request, 'forbidden.html')


def search_view(request):
    context = {}

    if request.method == 'POST':
        prod_query = request.POST['prod_query']

        order_parameter = request.POST['order_parameter']
        if order_parameter == 'placeholder':
            order_parameter = 'title'
        if prod_query == '':
            products_retrieved = Product.objects.all().filter(quantity__gt=0)
            context['order_parameter'] = order_parameter
            context['products'] = products_retrieved
        else:
            products_retrieved = Product.objects.filter(title__contains=prod_query, quantity__gt=0)
            context['order_parameter'] = order_parameter
            context['products'] = products_retrieved

        context['query'] = prod_query

    return render(request, 'search.html', context)
