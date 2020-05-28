"""Product forms module."""

from django import forms
from django.forms import modelformset_factory
from django.forms.models import inlineformset_factory
from cashier.forms.base import CustomModelForm
from cashier.models import Product, HargaBertingkat, ConvertBarang


class DashProductForm(forms.ModelForm):
    """Custom product form."""

    class Meta:  # noqa D106
        model = Product
        fields = '__all__'
        # exclude = ('supplier', )

HargaBertingkatFormset = modelformset_factory(
    HargaBertingkat,
    fields=('min_quantity', 'max_quantity', 'price', ),
    extra=1,
)

class DashProductHargaBertingkatForm(forms.ModelForm):
    """Product Harga Bertingkat Form."""
    class Meta:
        model = HargaBertingkat
        exclude = ()

HargaBertingkatInlineFormset = inlineformset_factory(
    Product,
    HargaBertingkat,
    form=DashProductHargaBertingkatForm,
    fields=['max_quantity', 'min_quantity', 'price'],
    extra=1,
    can_delete=True
)

class DashProductUpdateForm(CustomModelForm):
    """CmsProductUpdateForm."""

    class Meta:  # noqa D106
        model = Product
        fields = '__all__'


class DashHargaBertingkatCreationForm(forms.ModelForm):
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