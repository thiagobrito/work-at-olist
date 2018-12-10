from datetime import timedelta


class PhoneCallPriceCalculator:
    _standing_charge = 0.36
    _call_minute_charge = 0.09

    def calculate(self, call_data):
        return self._standing_charge + \
               (self._calculate_payable_minutes(call_data['start'].time_stamp, call_data['end'].time_stamp) *
                self._call_minute_charge)

    def _calculate_payable_minutes(self, start_date_time, end_date_time):
        payable_minutes = 0

        free_start_time = start_date_time.replace(hour=22, minute=0, second=0)
        free_end_time = start_date_time.replace(hour=6, minute=0, second=0) + timedelta(days=1)
        morning_free_start_time = free_start_time - timedelta(days=1)
        morning_free_end_time = free_start_time.replace(hour=6, minute=0, second=0, day=free_start_time.day)

        payable_seconds = (end_date_time - start_date_time).total_seconds()

        # The user spent all night long connected or the call is inside free morning period (0AM to 6AM)
        if start_date_time <= free_start_time <= free_end_time <= end_date_time or \
                start_date_time <= morning_free_end_time <= end_date_time:
            payable_seconds -= self._calculate_free_seconds(start_date_time, end_date_time)

        # The user got some free time but not all night long
        elif start_date_time <= free_start_time <= end_date_time:
            payable_seconds = (free_start_time - start_date_time).total_seconds()

        # The full call is inside a free time or Morning calls (Eg.: started before 6AM)
        # must check the free call started a day before
        elif free_start_time <= start_date_time <= end_date_time <= free_end_time or \
                morning_free_start_time <= start_date_time <= end_date_time <= morning_free_end_time:
            payable_seconds = 0

        # We only pay for full minutes. If it's less than one minute call it won't have the minutes charged
        payable_minutes += int(payable_seconds / 60)

        return payable_minutes

    def _calculate_free_seconds(self, start_date_time, end_date_time):
        free_seconds = 0

        for day in range(0, (end_date_time - start_date_time).days + 1):
            current_day_start_date_time = start_date_time + timedelta(days=day)

            free_start_time = current_day_start_date_time.replace(hour=22, minute=0, second=0)
            free_end_time = current_day_start_date_time.replace(hour=6, minute=0, second=0) + timedelta(days=1)
            morning_free_end_time = free_start_time.replace(hour=6, minute=0, second=0, day=free_start_time.day)

            # The user spent all night long connected
            if current_day_start_date_time <= free_start_time <= free_end_time <= end_date_time:
                free_seconds += (free_end_time - free_start_time).total_seconds()

            # The user got some free time but not all night long
            elif current_day_start_date_time <= free_start_time <= end_date_time:
                free_seconds += (end_date_time - free_start_time).total_seconds()

            # The call is inside free morning period (0AM to 6AM)
            elif current_day_start_date_time <= morning_free_end_time <= end_date_time:
                free_seconds += (morning_free_end_time - current_day_start_date_time).total_seconds()

        return free_seconds
