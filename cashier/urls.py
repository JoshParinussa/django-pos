"""Buildr url module."""
from django.urls import path

from cashier.views import dash as dash_view
from cashier.views.dash import account as account_view
from cashier.views.dash import product as dash_product_view

urlpatterns = [
    path('', account_view.Login.as_view(), name="login"),
    path('dash/',
         dash_view.DashHomeView.as_view(),
         name='dash_view'),

    # ADMIN PRODUCT
    path('dash/products', dash_product_view.ProductListView.as_view(), name='dash_product_list'),
    path('dash/products/create', dash_product_view.ProductCreateView.as_view(), name='dash_product_create'),
]
