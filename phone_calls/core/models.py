from datetime import timedelta

from django.db import models

from phone_calls.core.validators import phone_number_validator, price_validator


class PhoneRecord(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField('type', max_length=12)
    time_stamp = models.DateTimeField()
    call_id = models.IntegerField()
    source = models.CharField(max_length=12, validators=[phone_number_validator])
    destination = models.CharField(max_length=12, validators=[phone_number_validator])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.save_bill()

    def save_bill(self):
        """
        Identify pair call (end if it's start call or start if it's end call) and insert call information inside phone bill
        """
        pair_type = 'end' if self.type == 'start' else 'start'
        pair_call = PhoneRecord.objects.filter(call_id=self.call_id, type=pair_type)

        if pair_call.exists():
            self.full_clean()

            call_data = {pair_type: pair_call.get(), self.type: self}
            PhoneBill().calculate_and_save(call_data=call_data)


class PhoneBill(models.Model):
    id = models.AutoField(primary_key=True)
    destination = models.CharField(max_length=12, validators=[phone_number_validator])
    start_time_stamp = models.DateTimeField()
    duration = models.PositiveIntegerField()
    price = models.FloatField(validators=[price_validator])

    _standing_charge = 0.36
    _call_minute_charge = 0.09

    def calculate_and_save(self, call_data):
        data = {'destination': call_data['start'].destination, 'start_time_stamp': call_data['start'].time_stamp,
                'duration': self._calculate_duration(call_data), 'price': self._calculate_price(call_data)}

        if data['price'] > 0:
            return PhoneBill.objects.create(**data)

    def _calculate_duration(self, call_data):
        return (call_data['end'].time_stamp - call_data['start'].time_stamp).total_seconds()

    def _calculate_price(self, call_data):
        return self._standing_charge + (self._calculate_payable_minutes(call_data) * self._call_minute_charge)

    def _calculate_payable_minutes(self, call_data):
        payable_minutes = 0
        start_date_time = call_data['start'].time_stamp
        end_date_time = call_data['end'].time_stamp

        free_start_time = start_date_time.replace(hour=22, minute=0, second=0)
        free_end_time = start_date_time.replace(hour=6, minute=0, second=0) + timedelta(days=1)
        morning_free_start_time = free_start_time - timedelta(days=1)
        morning_free_end_time = free_start_time.replace(hour=6, minute=0, second=0, day=free_start_time.day)

        payable_seconds = (call_data['end'].time_stamp - call_data['start'].time_stamp).total_seconds()

        # The user spent all night long connected or the call is inside free morning period (0AM to 6AM)
        if start_date_time <= free_start_time <= free_end_time <= end_date_time or \
                start_date_time <= morning_free_end_time <= end_date_time:
            payable_seconds -= self._calculate_free_seconds(call_data)

        # The user got some free time but not all night long
        elif start_date_time <= free_start_time <= end_date_time:
            payable_seconds = (free_start_time - call_data['start'].time_stamp).total_seconds()

        # The full call is inside a free time or Morning calls (Eg.: started before 6AM)
        # must check the free call started a day before
        elif free_start_time <= start_date_time <= end_date_time <= free_end_time or \
                morning_free_start_time <= start_date_time <= end_date_time <= morning_free_end_time:
            payable_seconds = 0

        # We only pay for full minutes. If it's less than one minute call it won't have the minutes charged
        payable_minutes += int(payable_seconds / 60)

        return payable_minutes

    def _calculate_free_seconds(self, call_data):
        free_seconds = 0

        start_date_time = call_data['start'].time_stamp
        end_date_time = call_data['end'].time_stamp

        for day in range(0, (end_date_time - start_date_time).days + 1):
            start_date_time = call_data['start'].time_stamp + timedelta(days=day)

            free_start_time = start_date_time.replace(hour=22, minute=0, second=0)
            free_end_time = start_date_time.replace(hour=6, minute=0, second=0) + timedelta(days=1)
            morning_free_end_time = free_start_time.replace(hour=6, minute=0, second=0, day=free_start_time.day)

            # The user spent all night long connected
            if start_date_time <= free_start_time <= free_end_time <= end_date_time:
                free_seconds += (free_end_time - free_start_time).total_seconds()

            # The user got some free time but not all night long
            elif start_date_time <= free_start_time <= end_date_time:
                free_seconds += (end_date_time - free_start_time).total_seconds()

            # The call is inside free morning period (0AM to 6AM)
            elif start_date_time <= morning_free_end_time <= end_date_time:
                free_seconds += (morning_free_end_time - start_date_time).total_seconds()

        return free_seconds
