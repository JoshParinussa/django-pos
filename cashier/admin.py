"""Django admin module."""
from django.contrib import admin

from cashier.models import (Pembayaran, PembayaranProduct, Product,
                            ProductCategory, HargaBertingkat, ConvertBarang, User)


class UserAdmin(admin.ModelAdmin):
    """UserAdmin."""
    pass


class PembayaranAdmin(admin.ModelAdmin):
    """PembayaranAdmin."""
    pass


class PembayaranProductAdmin(admin.ModelAdmin):
    """PembayaranProductAdmin."""
    pass


class ProductAdmin(admin.ModelAdmin):
    """ProductAdmin."""
    pass


class ProductCategoryAdmin(admin.ModelAdmin):
    """ProductCategoryAdmin."""
    pass


class HargaBertingkatAdmin(admin.ModelAdmin):
    """HargaBertingkatAdmin."""
    pass


class ConvertBarangAdmin(admin.ModelAdmin):
    """ConvertBarangAdmin."""
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Pembayaran, PembayaranAdmin)
admin.site.register(PembayaranProduct, PembayaranProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(HargaBertingkat, HargaBertingkatAdmin)
admin.site.register(ConvertBarang, ConvertBarangAdmin)
