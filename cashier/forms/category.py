"""Product forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import ProductCategory


class DashProductCategoryCreationForm(CustomModelForm):
    """Custom product creation form."""

    class Meta:  # noqa D106
        model = ProductCategory
        fields = ("name", )


class DashProductCategoryUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = ProductCategory
        fields = ("name", )
