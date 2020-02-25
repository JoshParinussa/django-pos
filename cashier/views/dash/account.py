"""User authorisation module."""
from django.contrib.auth import views as account_views
from django.shortcuts import resolve_url


class Login(account_views.LoginView):
    """Login view."""
    redirect_authenticated_user = True

    def get_success_url(self):
        """Override get_success_url."""
        url = self.get_redirect_url()

        user = self.request.user

        if user.is_superuser:
            return url or resolve_url('dash_view')
