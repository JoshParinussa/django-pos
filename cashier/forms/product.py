"""Product forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Product, HargaBertingkat, ConvertBarang


class DashProductCreationForm(CustomModelForm):
    """Custom product creation form."""

    class Meta:  # noqa D106
        model = Product
        fields = '__all__'


class DashProductUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Product
        fields = '__all__'


class DashHargaBertingkatCreationForm(CustomModelForm):
    """DashHargaBertingkatCreationForm."""

    class Meta:  # noqa D106
        model = HargaBertingkat
        fields = '__all__'

class DashConvertBarangCreationForm(CustomModelForm):
    """DashConvertBarangCreationForm."""

    class Meta:  # noqa D106
        model = ConvertBarang
        fields = '__all__'

class DashConvertBarangUpdateForm(CustomModelForm):
    """DashConvertBarangUpdateForm."""

    class Meta:  # noqa D106
        model = ConvertBarang
        fields = '__all__'