"""Product views."""
from cashier.forms.user import DashUserCreationForm, DashUserUpdateForm
from django.contrib.auth import get_user_model
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


class UserDeleteView(DashUserMixin, DashDeleteView):
    """UserDeleteView."""
    model = User
    template_name = 'dash/user/delete.html'
    success_message = 'User %(email)s deleted successfully'
