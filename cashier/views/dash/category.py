"""Product views."""
from cashier.forms import category as category_forms
from cashier.models import ProductCategory
from cashier.views.dash.base import DashCreateView, DashListView, DashUpdateView


class DashCategoryMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class ProductCategoryListView(DashCategoryMixin, DashListView):
    """BrandListView."""
    template_name = 'dash/category/list.html'
    model = ProductCategory


class ProductCategoryCreateView(DashCategoryMixin, DashCreateView):
    """ProductCreateView."""
    model = ProductCategory
    form_class = category_forms.DashProductCategoryCreationForm
    template_name = 'dash/category/create.html'


class ProductCategoryUpdateView(DashCategoryMixin, DashUpdateView):
    """ProductUpdateView."""
    model = ProductCategory
    form_class = category_forms.DashProductCategoryUpdateForm
    template_name = 'dash/category/update.html'
