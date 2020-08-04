import logging
from datetime import date, datetime

import pytz
from pytz import timezone
from django.views.generic import TemplateView

from cashier.models import Invoice, Purchase, Income, Expense
from cashier.views.dash.base import DashListView, BaseUserPassesTestMixin, ManageBaseView
from cashier.services.member import member_services

class ReportProfitLossView(DashListView, BaseUserPassesTestMixin):
    template_name = "dash/report/profit_loss.html"
    model = Invoice

