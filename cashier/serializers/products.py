"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Product, ConvertBarang
from django_restql.mixins import DynamicFieldsMixin


class ProductSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    """Products Serializer."""
    text = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name', read_only=True)
    unit = serializers.CharField(source='unit.name', read_only=True)


    def get_text(self, obj):
        return '{item} Rp. {selling_price}'.format(item=obj.name, selling_price=f"{int(obj.selling_price):,d}") 

    class Meta:  # noqa D106
        model = Product
        name = 'product'
        fields = '__all__'
        datatables_always_serialize = ('id')

class ConvertBarangSerializer(serializers.ModelSerializer):
    """ConvertBarangSerializer."""
    product = serializers.CharField(source='product.name', read_only=True)
    unit = serializers.CharField(source='unit.name', read_only=True)
    
    class Meta:  # noqa D106
        model = ConvertBarang
        name = 'convertbarang'
        fields = '__all__'
        # datatables_always_serialize = ('id','product','unit_id','quantity','purchase_price','selling_price','grosir_1_price','grosir_2_price','grosir_3_price')