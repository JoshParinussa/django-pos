"""SupplierServices module."""
from cashier.models import Supplier


class SupplierServices:
    """SupplierServices."""
    def get_suppliers_list(self):
        suppliers = Supplier.objects.all()
        return suppliers

    def get_supplier_by_id(self, id):
        try:
            supplier = Supplier.objects.filter(id=id).first()
        except Exception as e:
            supplier = None
        return supplier
        


supplier_services = SupplierServices()
