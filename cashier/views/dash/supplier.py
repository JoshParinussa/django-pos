"""Product views."""
from cashier.forms import supplier as supplier_forms
from cashier.models import Supplier
from cashier.views.dash.base import (DashCreateView, DashDeleteView,
                                     DashListView, DashUpdateView)
from cashier.services.common import common_services


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


class ReportListSupplierView(DashSupplierMixin, DashListView):
    """ExpenseListView."""
    template_name = 'dash/report/supplier/list.html'
    model = Supplier


class ReportSupplierView(DashSupplierMixin, DashListView):
    """ExpenseListView."""
    template_name = 'dash/report/supplier/supplier.html'
    model = Supplier

    def get_context_data(self, **kwargs):
        dates = self.request.GET.getlist('dates[0]') + self.request.GET.getlist('dates[1]')
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        supplier_kode = Supplier.objects.get(id=pk)
        context['pk'] = pk
        context['supplier_kode'] = supplier_kode
        context['dates'] = dates
        return context