"""Product forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Product, HargaBertingkat


class DashProductCreationForm(CustomModelForm):
    """Custom product creation form."""

    class Meta:  # noqa D106
        model = Product
        fields = '__all__'


class DashProductUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Product
        fields = ("name", "barcode", "category", "stock")


class DashHargaBertingkatCreationForm(CustomModelForm):
    """DashHargaBertingkatCreationForm."""

    class Meta:  # noqa D106
        model = HargaBertingkat
        fields = '__all__'