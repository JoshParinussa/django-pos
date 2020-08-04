"""Product Model."""
from django.db import models

from .base import BaseModel


OPERATOR_TINGKAT_CHOICES = [
    ('0', '>='),
    ('1', '<='),
    ('2', '>'),
    ('3', '<'),
]

class ProductStatus(models.IntegerChoices):
    """StoreTier choice."""
    ACTIVE = 0
    INACTIVE = 1


class Product(BaseModel):
    """Product model."""
    name = models.CharField(max_length=128, verbose_name="nama produk")
    barcode = models.CharField(max_length=128, blank=False, null=False, unique=True)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, verbose_name="kategori", blank=True, null=True)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, null=True, verbose_name="satuan")
    stock = models.BigIntegerField(blank=True, null=True, verbose_name="stok")
    minimal_stock = models.BigIntegerField(blank=True, null=True, verbose_name="batas minimal")
    purchase_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, verbose_name="harga beli")
    selling_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, verbose_name="eceran")
    grosir_1 = models.DecimalField(max_digits=9, decimal_places=0, blank=True, null=True)
    grosir_2 = models.DecimalField(max_digits=9, decimal_places=0, blank=True, null=True)
    grosir_3 = models.DecimalField(max_digits=9, decimal_places=0, blank=True, null=True)

    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, blank=True, null=True)

    status = models.PositiveSmallIntegerField(choices=ProductStatus.choices, default=ProductStatus.ACTIVE, db_index=True)

    def __str__(self):
        """String representation."""
        return self.name


class Unit(BaseModel):
    """Unit."""
    name = models.CharField(max_length=128, verbose_name="nama satuan")

    def __str__(self):
        """String representation."""
        return self.name


class ProductCategory(BaseModel):
    """ProductCategory model."""
    name = models.CharField(max_length=128, db_index=True, verbose_name="nama kategori")

    def __str__(self):
        """String representation."""
        return self.name


class HargaBertingkat(BaseModel):
    """HargaBertingkat."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='hargabertingkat')
    min_quantity = models.IntegerField(blank=True, null=True, verbose_name="min qty")
    # max_quantity = models.IntegerField(blank=True, null=True, verbose_name="max qty")
    price = models.DecimalField(max_digits=9, decimal_places=0, null=True, verbose_name="harga jual")

    def __str__(self):
        """String representation."""
        return self.product.name


class ConvertBarang(BaseModel):
    """ConvertBarang."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='convert_barang', verbose_name="produk")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True, verbose_name="satuan")
    quantity = models.IntegerField(blank=False, null=False, verbose_name="kuantiti")
    purchase_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, verbose_name="harga beli")
    selling_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, verbose_name="harga jual")
    grosir_1_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    grosir_2_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    grosir_3_price = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
