"""Income forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Income


class DashIncomeCreationForm(CustomModelForm):
    """Custom income creation form."""

    class Meta:  # noqa D106
        model = Income
        fields = ('keterangan', 'jumlah_pemasukan', )


class DashIncomeUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Income
        fields = ('keterangan', 'jumlah_pemasukan', )