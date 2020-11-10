"""card_ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views, settings
from django.conf.urls.static import static
from user_management import views as v
from .views import search_view, forbidden_view

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('base', views.base, name='base'),
                  path('home', views.home, name='home'),
                  path('register', v.register, name='register'),
                  path('search/', search_view, name='search'),
                  path('forbidden/', forbidden_view, name='forbidden'),
                  path('', include('user_management.urls', namespace='user_management')),
                  path('', include('shop.urls', namespace='shop')),
                  path('', include('product.urls', namespace='product')),
                  path('', include('cart.urls', namespace='shopping_cart')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
