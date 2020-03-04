"""User Api view."""
from django.contrib.auth import get_user_model

from cashier.serializers.user import UserSerializer
from rest_framework import viewsets

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """UserViewSet."""
    serializer_class = UserSerializer
    queryset = User.objects.order_by('email')
