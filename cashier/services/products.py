"""ProductServices module."""
from cashier.models import Product


class ProductServices:
    """ProductServices."""
    def get_harga_bertingkat(self, product, qty):
        harga_bertingkats = product.hargabertingkat.all().order_by('max_quantity')
        found = False
        if harga_bertingkats:
            for harga_bertingkat in harga_bertingkats:
                if harga_bertingkat.min_quantity <= qty <= harga_bertingkat.max_quantity:
                    harga = harga_bertingkat.price
                    found = True
                    break
            if found is False:
                if qty > harga_bertingkats.last().max_quantity:
                    harga = harga_bertingkats.last().price
                else:
                    harga = product.selling_price
        else:
            harga = product.selling_price
        return harga


product_services = ProductServices()
