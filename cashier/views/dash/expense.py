"""Product views."""
from cashier.forms import expense as expense_forms
from cashier.models import Expense
from cashier.views.dash.base import (DashCreateView, DashDeleteView, DashListView, DashUpdateView)  
from datetime import datetime, date


class DashExpenseMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class ExpenseListView(DashExpenseMixin, DashListView):
    """ExpenseListView."""
    template_name = 'dash/expense/list.html'
    model = Expense


class ExpenseCreateView(DashExpenseMixin, DashCreateView):
    """ExpenseCreateView."""
    model = Expense
    form_class = expense_forms.DashExpenseCreationForm
    template_name = 'dash/expense/create.html'

    def form_valid(self, form):
        form.instance.cashier = self.request.user
        return super().form_valid(form)


class ExpenseUpdateView(DashExpenseMixin, DashUpdateView):
    """ExpenseUpdateView."""
    model = Expense
    form_class = expense_forms.DashExpenseUpdateForm
    template_name = 'dash/expense/update.html'


class ExpenseDeleteView(DashExpenseMixin, DashDeleteView):
    """ExpenseDeleteView."""
    model = Expense
    template_name = 'dash/expense/delete.html'
