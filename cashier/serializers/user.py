"""User serializer module."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer class."""

    class Meta:  # noqa D106
        model = User
        name = 'user'
        fields = '__all__'
        datatables_always_serialize = ('id', 'email')
