from django.db import models

from .base import BaseModel

class Supplier(BaseModel):
    """Supplier model."""
    company_name = models.CharField(max_length=128, db_index=True)
    address = models.CharField(max_length=128, db_index=True)
    contact_person =  models.CharField(max_length=128, db_index=True)
    office_phone = models.CharField(max_length=128, blank=False, null=False)
    phone = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self):
        """String representation."""
        return self.company_name