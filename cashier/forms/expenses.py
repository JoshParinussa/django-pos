"""Expenses forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Expenses


class DashExpensesCreationForm(CustomModelForm):
    """Custom product creation form."""

    class Meta:  # noqa D106
        model = Expenses
        fields = ('information', 'cost', )


class DashExpensesUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Expenses
        fields = ('information', 'cost', )