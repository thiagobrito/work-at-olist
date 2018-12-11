import locale
import time
from datetime import datetime

from rest_framework import serializers


# Expected format: R$ 01,36
from rest_framework.fields import DateTimeField


class MoneyBrlField(serializers.Field):
    def to_representation(self, price):
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(price)

    def to_internal_value(self, price):
        return price


# Expected format: 0h35m42s
class DurationField(serializers.Field):
    def to_representation(self, duration):
        return time.strftime('%Hh%Mm%Ss', time.gmtime(duration))

    def to_internal_value(self, duration):
        return int(duration)


# Separate one field "start_time_stamp" to two "start_time" and "start_date"
class SeparatedDateTimeFields(serializers.DateTimeField):
    def to_representation(self, start_time_stamp):
        ret = {
            'start_time': '%02d:%02d:%02d' % (start_time_stamp.hour, start_time_stamp.minute, start_time_stamp.second),
            'start_date': '%02d/%02d/%04d' % (start_time_stamp.day, start_time_stamp.month, start_time_stamp.year)
        }
        return ret
