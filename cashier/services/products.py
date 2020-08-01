"""ProductServices module."""
from cashier.models import Product


class ProductServices:
    """ProductServices."""
    # def get_harga_bertingkat(self, product, qty):
    #     harga_bertingkats = product.hargabertingkat.all().order_by('max_quantity')
    #     found = False
    #     if harga_bertingkats:
    #         for harga_bertingkat in harga_bertingkats:
    #             if harga_bertingkat.min_quantity <= qty <= harga_bertingkat.max_quantity:
    #                 harga = harga_bertingkat.price
    #                 found = True
    #                 break
    #         if found is False:
    #             if qty > harga_bertingkats.last().max_quantity:
    #                 harga = harga_bertingkats.last().price
    #             else:
    #                 harga = product.selling_price
    #     else:
    #         harga = product.selling_price
    #     return harga

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
        return product.selling_price

    def check_product_stock(self, product, qty):
        """get_product_stock."""
        is_out_of_stock = True
        if int(qty) <= product.stock :
            is_out_of_stock = False
        return is_out_of_stock


product_services = ProductServices()
