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

    def check_product_stock(self, product, qty):
        """get_product_stock."""
        is_out_of_stock = True
        if product.stock >= int(qty):
            is_out_of_stock = False
        print("# STOCK", product.stock, qty)
        return is_out_of_stock


product_services = ProductServices()
