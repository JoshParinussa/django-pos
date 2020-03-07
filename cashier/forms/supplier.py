"""Supplier forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Supplier


class DashSupplierCreationForm(CustomModelForm):
    """Custom product creation form."""

    class Meta:  # noqa D106
        model = Supplier
        fields = '__all__'


class DashSupplierUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Supplier
        fields = ("company_name", "address", "contact_person", "office_phone", "phone")