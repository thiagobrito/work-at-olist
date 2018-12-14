from decimal import *
from datetime import timedelta

from phone_calls.core.period import Period


class PhoneCallPriceCalculator:
    standing_charge = Decimal(0.36)
    call_minute_charge = Decimal(0.09)

    @classmethod
    def calculate(cls, call_period):
        instance = cls()
        return instance.standing_charge + \
               (instance._calculate_payable_minutes(call_period) * instance.call_minute_charge)

    def _calculate_payable_minutes(self, call_period):
        # We only pay for full minutes. If it's less than one minute call it won't have the minutes charged
        return int((call_period.seconds_diff() - self._calculate_free_seconds(call_period)) / 60)

    def _calculate_free_seconds(self, call_period):
        free_seconds = 0

        for day in range(0, (call_period.end - call_period.start).days + 1):
            current_day = Period(call_period.start + timedelta(days=day), call_period.end + timedelta(days=day))
            free = Period(current_day.start.replace(hour=22, minute=0, second=0),
                          current_day.start.replace(hour=6, minute=0, second=0) + timedelta(days=1))
            free_previous_day = Period(free.start - timedelta(days=1), free.end - timedelta(days=1))

            # The call is inside free time in the morning or free night previous day
            if free_previous_day.is_moment_inside(current_day.start):
                free_seconds += (free_previous_day.end - current_day.start).total_seconds()

            # The call is all inside free time
            elif current_day.is_inside(free.start, free.end):
                free_seconds += current_day.seconds_diff()

            # The user spent all night long connected
            elif free.is_inside(current_day.start, call_period.end):
                free_seconds += free.seconds_diff()

            # The user got some free time but not all night long
            elif Period(current_day.start, call_period.end).is_moment_inside(free.start):
                free_seconds += (call_period.end - free.start).total_seconds()

        return free_seconds
