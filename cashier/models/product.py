"""Product Model."""
from django.db import models

from .base import BaseModel


class Product(BaseModel):
    """Product model."""
    name = models.CharField(max_length=128, db_index=True)
    barcode = models.CharField(max_length=128, blank=False, null=False)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)
    unit = models.ForeignKey('Unit', on_delete=models.CASCADE, null=True)
    stock = models.PositiveIntegerField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=9, decimal_places=0, null=True)
    selling_price = models.DecimalField(max_digits=9, decimal_places=0, null=True)

    quantity_grosir_1 = models.IntegerField(blank=False, null=True)
    grosir_1_price = models.DecimalField(max_digits=9, decimal_places=0, null=True)
    quantity_grosir_2 = models.IntegerField(blank=False, null=True)
    grosir_2_price = models.DecimalField(max_digits=9, decimal_places=0, null=True)
    quantity_grosir_3 = models.IntegerField(blank=False, null=True)
    grosir_3_price = models.DecimalField(max_digits=9, decimal_places=0, null=True)

    def __str__(self):
        """String representation."""
        return self.name


class Unit(BaseModel):
    """Unit."""
    name = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        """String representation."""
        return self.name


class ProductCategory(BaseModel):
    """ProductCategory model."""
    name = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        """String representation."""
        return self.name


class HargaBertingkat(BaseModel):
    """HargaBertingkat."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)
    selling_price = models.DecimalField(max_digits=9, decimal_places=0, null=True)


class ConvertBarang(BaseModel):
    """ConvertBarang."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(blank=False, null=False)
    selling_price = models.DecimalField(max_digits=9, decimal_places=0, null=True)
