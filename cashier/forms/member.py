"""Member forms module."""

from cashier.forms.base import CustomModelForm
from cashier.models import Member


class DashMemberCreationForm(CustomModelForm):
    """Custom member creation form."""

    class Meta:  # noqa D106
        model = Member
        fields = '__all__'


class DashMemberUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Member
        fields = '__all__'