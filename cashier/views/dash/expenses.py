"""Product views."""
from cashier.forms import expenses as expenses_forms
from cashier.models import Expenses
from cashier.views.dash.base import (DashCreateView, DashDeleteView, DashListView, DashUpdateView)  
from datetime import datetime, date


class DashExpensesMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class ExpensesListView(DashExpensesMixin, DashListView):
    """ExpensesListView."""
    template_name = 'dash/expenses/list.html'
    model = Expenses


class ExpensesCreateView(DashExpensesMixin, DashCreateView):
    """ExpensesCreateView."""
    model = Expenses
    form_class = expenses_forms.DashExpensesCreationForm
    template_name = 'dash/expenses/create.html'


class ExpensesUpdateView(DashExpensesMixin, DashUpdateView):
    """ExpensesUpdateView."""
    model = Expenses
    form_class = expenses_forms.DashExpensesUpdateForm
    template_name = 'dash/expenses/update.html'


class ExpensesDeleteView(DashExpensesMixin, DashDeleteView):
    """ExpensesDeleteView."""
    model = Expenses
    template_name = 'dash/expenses/delete.html'
