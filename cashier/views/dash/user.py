"""Product views."""
# from cashier.forms import product as product_forms
from django.contrib.auth import get_user_model
from cashier.views.dash.base import DashCreateView, DashListView

User = get_user_model()


class DashUserMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class UserListView(DashUserMixin, DashListView):
    """BrandListView."""
    template_name = 'dash/user/list.html'
    model = User


# class UserCreateView(DashUserMixin, DashCreateView):
#     """ProductCreateView."""
#     model = Product
#     form_class = product_forms.DashProductCreationForm
#     template_name = 'dash/product/create.html'
