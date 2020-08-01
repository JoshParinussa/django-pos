"""ProductServices module."""
from cashier.models import Product

class SaleServices:
    """SaleServices."""
    def get_harga_bertingkat_price(self, product, qty):
        harga_bertingkats = product.hargabertingkat.order_by('min_quantity')

        for i, y in enumerate(harga_bertingkats):
            if int(harga_bertingkats.first().min_quantity) <= qty <= int(y.min_quantity):
                if y.min_quantity > qty:
                    return harga_bertingkats[i - 1].price
            
            elif qty >= int(harga_bertingkats.last().min_quantity):
                return harga_bertingkats.last().price
            
            elif qty < int(harga_bertingkats.first().min_quantity) :
                return product.selling_price

sale_services = SaleServices()
