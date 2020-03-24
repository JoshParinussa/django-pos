"""Product views."""
from cashier.forms import supplier as supplier_forms
from cashier.models import Supplier
from cashier.views.dash.base import (DashCreateView, DashDeleteView,
                                     DashListView, DashUpdateView)


class DashSupplierMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class SupplierListView(DashSupplierMixin, DashListView):
    """SupplierListView."""
    template_name = 'dash/supplier/list.html'
    model = Supplier


class SupplierCreateView(DashSupplierMixin, DashCreateView):
    """SupplierCreateView."""
    model = Supplier
    form_class = supplier_forms.DashSupplierCreationForm
    template_name = 'dash/supplier/create.html'


class SupplierUpdateView(DashSupplierMixin, DashUpdateView):
    """UnitUpdateView."""
    model = Supplier
    form_class = supplier_forms.DashSupplierUpdateForm
    template_name = 'dash/supplier/update.html'


class SupplierDeleteView(DashSupplierMixin, DashDeleteView):
    """UnitUpdateView."""
    model = Supplier
    template_name = 'dash/supplier/delete.html'
