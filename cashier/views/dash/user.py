"""Product views."""
from django.contrib.auth import views as account_views
from django.contrib.auth import views as site_views
from cashier.forms.user import DashUserCreationForm, DashUserUpdateForm
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from cashier.views.dash.base import DashCreateView, DashListView, DashUpdateView, DashDeleteView, BaseUserPassesTestMixin

User = get_user_model()


class DashUserMixin(BaseUserPassesTestMixin):
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class UserListView(DashUserMixin, DashListView):
    """BrandListView."""
    template_name = 'dash/user/list.html'
    model = User


class UserCreateView(DashUserMixin, DashCreateView):
    """UserCreateView."""
    model = User
    form_class = DashUserCreationForm
    template_name = 'dash/user/create.html'


class UserUpdateView(DashUserMixin, DashUpdateView):
    """UserUpdateView."""
    model = User
    form_class = DashUserUpdateForm
    template_name = 'dash/user/update.html'
    success_message = 'User %(email)s updated successfully'

    def get_context_data(self, **kwargs):
        """Override get context."""
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        """Override form valid."""
        user = form.save(commit=False)
        new_password = form.cleaned_data['password1']
        if new_password:
            user.set_password(new_password)
        user.save()
        
        return super(UserUpdateView, self).form_valid(form)


class UserDeleteView(DashUserMixin, DashDeleteView):
    """UserDeleteView."""
    model = User
    template_name = 'dash/user/delete.html'
    success_message = 'User %(email)s deleted successfully'


class ChangePasswordView(account_views.PasswordChangeView):
    """Change password."""
    model = User
    template_name = 'dash/user/change_password.html'
    # success_url = reverse_lazy('dash_user_update')
    success_message = _('Password has been updated!')

    def get_form_kwargs(self):
        pk = self.kwargs['pk']
        print("# PK", pk)
        kwargs = super().get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.kwargs['pk'])
        return kwargs

    def get_context_data(self, **kwargs):
        """Override get context."""
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['object'] = User.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse_lazy('dash_user_update', kwargs={'pk': self.kwargs['pk']})