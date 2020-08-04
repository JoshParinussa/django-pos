"""Expenses forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Expense


class DashExpenseCreationForm(CustomModelForm):
    """Custom product creation form."""

    class Meta:  # noqa D106
        model = Expense
        fields = ('information', 'cost', )


class DashExpenseUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Expense
        fields = ('information', 'cost', )