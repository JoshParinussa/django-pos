"""User authorisation module."""
from django.contrib.auth import views as account_views
from django.shortcuts import resolve_url
from django.urls import resolve


class Login(account_views.LoginView):
    """Login view."""

    def get_success_url(self):
        """Override get_success_url."""
        url = self.get_redirect_url()
        return url or resolve_url('admin_view')
