"""Product Model."""
from django.db import models

from .base import BaseModel


class Product(BaseModel):
    """Product model."""
    name = models.CharField(max_length=128, db_index=True)
    barcode = models.CharField(max_length=128, blank=False, null=False)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField(blank=True, null=True)

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
    price = models.DecimalField(max_digits=9, decimal_places=0)

class ConvertBarang(BaseModel):
    """ConvertBarang."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, null=False)
    