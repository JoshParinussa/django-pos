"""Product views."""
from cashier.forms import income as income_forms
from cashier.models import Income
from cashier.views.dash.base import (DashCreateView, DashDeleteView, DashListView, DashUpdateView)  
from cashier.services.code_generator import code_generator
from datetime import datetime, date


class DashIncomeMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class IncomeListView(DashIncomeMixin, DashListView):
    """IncomeListView."""
    template_name = 'dash/income/list.html'
    model = Income


class IncomeCreateView(DashIncomeMixin, DashCreateView):
    """IncomeCreateView."""
    model = Income
    form_class = income_forms.DashIncomeCreationForm
    template_name = 'dash/income/create.html'

    def form_valid(self, form):
        form.instance.cashier = self.request.user
        form.instance.invoice = code_generator.generate(self.request.user, Income)
        return super().form_valid(form)

    


class IncomeUpdateView(DashIncomeMixin, DashUpdateView):
    """IncomeUpdateView."""
    model = Income
    form_class = income_forms.DashIncomeUpdateForm
    template_name = 'dash/income/update.html'

    def form_valid(self, form):
        form.instance.cashier = self.request.user
        return super().form_valid(form)


class IncomeDeleteView(DashIncomeMixin, DashDeleteView):
    """IncomeDeleteView."""
    model = Income
    template_name = 'dash/income/delete.html'

class ReportIncomeView(DashIncomeMixin, DashListView):
    """IncomeListView."""
    template_name = 'dash/report/income.html'
    model = Income