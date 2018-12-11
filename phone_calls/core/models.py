from django.db import models

from phone_calls.core.validators import phone_number_validator, price_validator
from phone_calls.core.price import PhoneCallPriceCalculator


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

    __phone_call_price_calculator = PhoneCallPriceCalculator()

    def calculate_and_save(self, call_data):
        data = {'destination': call_data['start'].destination, 'start_time_stamp': call_data['start'].time_stamp,
                'duration': self._calculate_duration(call_data), 'price': self._calculate_price(call_data)}

        if data['price'] > 0:
            return PhoneBill.objects.create(**data)

    def _calculate_duration(self, call_data):
        return (call_data['end'].time_stamp - call_data['start'].time_stamp).total_seconds()

    def _calculate_price(self, call_data):
        return self.__phone_call_price_calculator.calculate(call_data)
