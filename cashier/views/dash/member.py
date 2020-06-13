"""Product views."""
from cashier.forms import member as member_forms
from cashier.models import Member
from cashier.views.dash.base import (DashCreateView, DashDeleteView,
                                     DashListView, DashUpdateView)


class DashMemberMixin:
    """Mixin for define common attribute between classes."""

    def get_icon(self):
        """Get icon."""
        return 'flaticon-list-1'


class MemberListView(DashMemberMixin, DashListView):
    """MemberListView."""
    template_name = 'dash/member/list.html'
    model = Member


class MemberCreateView(DashMemberMixin, DashCreateView):
    """MemberCreateView."""
    model = Member
    form_class = member_forms.DashMemberCreationForm
    template_name = 'dash/member/create.html'


class MemberUpdateView(DashMemberMixin, DashUpdateView):
    """UnitUpdateView."""
    model = Member
    form_class = member_forms.DashMemberUpdateForm
    template_name = 'dash/member/update.html'


class MemberDeleteView(DashMemberMixin, DashDeleteView):
    """UnitUpdateView."""
    model = Member
    template_name = 'dash/member/delete.html'
