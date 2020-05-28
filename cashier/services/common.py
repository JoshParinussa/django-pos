"""CommonServices module."""
import datetime

import pytz
from django.utils import timezone


class CommonServices:
    """CommonServices."""
    def convert_date_to_utc(self, date_range):
        date_format = '%Y-%m-%d'
        unaware_start_date = datetime.datetime.strptime(date_range[0], date_format)
        unaware_start_date = datetime.datetime.combine(unaware_start_date, datetime.time.min)
        unaware_start_date = pytz.timezone('Asia/Jakarta').localize(unaware_start_date)
        aware_start_date = unaware_start_date.astimezone(pytz.timezone('UTC'))

        unaware_end_date = datetime.datetime.strptime(date_range[1], date_format)
        unaware_end_date = datetime.datetime.combine(unaware_end_date, datetime.time.max)
        unaware_end_date = pytz.timezone('Asia/Jakarta').localize(unaware_end_date)
        aware_end_date = unaware_end_date.astimezone(pytz.timezone('UTC'))

        result=[aware_start_date, aware_end_date]
        return result

common_services = CommonServices()
