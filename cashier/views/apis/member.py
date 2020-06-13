"""Member Api view."""
from cashier.models import Member
from cashier.serializers.member import MemberSerializer
from rest_framework import viewsets


class MemberViewSet(viewsets.ModelViewSet):
    """MemberViewSet."""
    serializer_class = MemberSerializer
    queryset = Member.objects.order_by('created_at')