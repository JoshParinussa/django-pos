"""Product Model."""
from django.db import models

from .base import BaseModel


class Product(BaseModel):
    """Product model."""
    name = models.CharField(max_length=128, db_index=True)
    barcode = models.CharField(max_length=128, blank=False, null=False)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name='products')
    stock = models.PositiveIntegerField(blank=True, null=False)

    def __str__(self):
        """String representation."""
        return self.name


class ProductCategory(BaseModel):
    """ProductCategory model."""
    name = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        """String representation."""
        return self.name
