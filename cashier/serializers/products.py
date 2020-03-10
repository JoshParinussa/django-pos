"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Product, ConvertBarang


class ProductSerializer(serializers.ModelSerializer):
    """Products Serializer."""
    category = serializers.CharField(source='category.name', read_only=True)
    unit = serializers.CharField(source='unit.name', read_only=True)

    class Meta:  # noqa D106
        model = Product
        name = 'product'
        fields = '__all__'

class ConvertBarangSerializer(serializers.ModelSerializer):
    """ConvertBarangSerializer."""
    product = serializers.CharField(source='product.name', read_only=True)
    unit = serializers.CharField(source='unit.name', read_only=True)
    
    class Meta:  # noqa D106
        model = ConvertBarang
        name = 'convertbarang'
        fields = '__all__'
        # datatables_always_serialize = ('id','product','unit_id','quantity','purchase_price','selling_price','grosir_1_price','grosir_2_price','grosir_3_price')
