"""Admin view."""
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


# @login_required(redirect_field_name=settings.LOGIN_URL)
class DashHomeView(LoginRequiredMixin, TemplateView):
    """DashHomeView."""
    login_url = settings.LOGIN_URL
    template_name = "dash/layout/base.html"

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user'] = self.request.user
        return context
