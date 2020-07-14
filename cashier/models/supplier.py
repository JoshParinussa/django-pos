from django.db import models

from .base import BaseModel

class Supplier(BaseModel):
    """Supplier model."""
    kode = models.CharField(max_length=32, db_index=True, blank=True, null=True)
    company_name = models.CharField(max_length=128, db_index=True, blank=True, null=True)
    address = models.CharField(max_length=128, db_index=True, blank=True, null=True)
    contact_person =  models.CharField(max_length=128, db_index=True, blank=True, null=True)
    office_phone = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        """String representation."""
        return self.kode