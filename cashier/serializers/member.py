"""Products serializer module."""
from rest_framework import serializers

from cashier.models import Member

class MemberSerializer(serializers.ModelSerializer):
    """Member Serializer."""

    class Meta:  # noqa D106
        model = Member
        name = 'member'
        fields = '__all__'
        datatables_always_serialize = ('id','name','address','phone','profession')