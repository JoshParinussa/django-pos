"""Django admin module."""
from django.contrib import admin

from cashier.models import (Pembayaran, PembayaranProduct, Product,
                            ProductCategory, HargaBertingkat, ConvertBarang,
                            User, Invoice, Sale, Supplier, Unit,
                            Purchase, PurchaseDetail)


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
    ordering = ['name']


class ProductCategoryAdmin(admin.ModelAdmin):
    """ProductCategoryAdmin."""
    pass


class HargaBertingkatAdmin(admin.ModelAdmin):
    """HargaBertingkatAdmin."""
    pass


class ConvertBarangAdmin(admin.ModelAdmin):
    """ConvertBarangAdmin."""
    pass


class InvoiceAdmin(admin.ModelAdmin):
    """InvoiceAdmin."""
    list_display = ("invoice", "created_at")
    ordering = ['-created_at']


class SaleAdmin(admin.ModelAdmin):
    """InvoiceAdmin."""
    pass

class SupplierAdmin(admin.ModelAdmin):
    """SupplierAdmin."""
    pass


class PurchaseAdmin(admin.ModelAdmin):
    """PurchaseAdmin."""
    pass


class PurchaseDetailAdmin(admin.ModelAdmin):
    """PurchaseDetaiAdmin."""
    pass


class UnitAdmin(admin.ModelAdmin):
    """UnitAdmin."""
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Pembayaran, PembayaranAdmin)
admin.site.register(PembayaranProduct, PembayaranProductAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(HargaBertingkat, HargaBertingkatAdmin)
admin.site.register(ConvertBarang, ConvertBarangAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PurchaseDetail, PurchaseDetailAdmin)
admin.site.register(Unit, UnitAdmin)
