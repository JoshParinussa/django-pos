"""Product views."""
from cashier.models import Product
from cashier.views.dash.base import (DashListView, DashCreateView)
from cashier.forms import product as product_forms


class DashProductMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class ProductListView(DashProductMixin, DashListView):
    """BrandListView."""
    template_name = 'dash/product/list.html'
    model = Product


class ProductCreateView(DashProductMixin, DashCreateView):
    """ProductCreateView."""
    model = Product
    form_class = product_forms.DashProductCreationForm
    template_name = 'dash/product/create.html'
