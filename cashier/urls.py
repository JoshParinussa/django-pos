"""Buildr url module."""
from django.urls import include, path
from django.contrib.auth import views
from cashier.views.admin import admin as admin_view
from cashier.views.admin import account as account_view

urlpatterns = [
    path('login/', account_view.Login.as_view(), name="login"),
    path('',
         admin_view.AdminHomeView.as_view(),
         name='admin_view'),
]
