"""User authorisation module."""
from django.contrib.auth import views as account_views
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.conf import settings


class Login(account_views.LoginView):
    """Login view."""
    redirect_authenticated_user = True

    def get_success_url(self):
        """Override get_success_url."""
        url = self.get_redirect_url()

        user = self.request.user

        if user.is_superuser or user.is_staff:
            return url or resolve_url('dash_view')


class LogoutView(account_views.LogoutView):
    """LogoutView."""
    next_page = reverse_lazy(settings.CASHIER_DASH_LOGOUT_REDIRECT_URL)
