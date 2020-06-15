"""ProductServices module."""
from cashier.models import Member


class MemberServices:
    """ProductServices."""
    def get_members_list(self):
        members = Member.objects.all()
        return members

    def get_member_by_id(self, id):
        try:
            member = Member.objects.filter(id=id).first()
        except Exception as e:
            member = None
        return member
        


member_services = MemberServices()
