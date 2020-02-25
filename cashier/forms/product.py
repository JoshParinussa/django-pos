"""Product forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Product


class DashProductCreationForm(CustomModelForm):
    """Custom product creation form."""

    class Meta:  # noqa D106
        model = Product
        fields = ("name", "barcode", "category", "stock")


class DashProductUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Product
        fields = ("name", "barcode", "category", "stock")
