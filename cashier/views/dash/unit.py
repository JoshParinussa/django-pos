"""Product views."""
from cashier.forms import unit as unit_forms
from cashier.models import Unit
from cashier.views.dash.base import DashCreateView, DashListView, DashUpdateView


class DashUnitMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class UnitListView(DashUnitMixin, DashListView):
    """UnitListView."""
    template_name = 'dash/unit/list.html'
    model = Unit


class UnitCreateView(DashUnitMixin, DashCreateView):
    """UnitCreateView."""
    model = Unit
    form_class = unit_forms.DashUnitCreationForm
    template_name = 'dash/unit/create.html'


class UnitUpdateView(DashUnitMixin, DashUpdateView):
    """UnitUpdateView."""
    model = Unit
    form_class = unit_forms.DashUnitCreationForm
    template_name = 'dash/unit/update.html'
