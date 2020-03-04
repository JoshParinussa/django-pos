"""Product forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Unit


class DashUnitCreationForm(CustomModelForm):
    """Custom product creation form."""

    class Meta:  # noqa D106
        model = Unit
        fields = ("name", )


class DashUnityUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Unit
        fields = ("name", )
