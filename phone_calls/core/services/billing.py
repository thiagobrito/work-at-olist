from django import forms

from phone_calls.core.services import Service
from phone_calls.core.models import *
from phone_calls.core.price import *


class CreateBilling(Service):
    type = forms.CharField()
    time_stamp = forms.DateTimeField()
    call_id = forms.IntegerField()
    source = forms.CharField()
    destination = forms.CharField()

    def process(self):
        type = self.cleaned_data['type']
        time_stamp = self.cleaned_data['time_stamp']
        call_id = self.cleaned_data['call_id']
        source = self.cleaned_data['source']
        destination = self.cleaned_data['destination']

        call = PhoneRecord.objects.create(
            type=type,
            time_stamp=time_stamp,
            call_id=call_id,
            source=source,
            destination=destination
        )

        self._save_billing_report(call)

        return call

    def clean(self):
        phone_number_validator(self.cleaned_data['source'])
        phone_number_validator(self.cleaned_data['destination'])

    def _save_billing_report(self, call):
        pair_type = 'end' if call.type == 'start' else 'start'
        pair_call = PhoneRecord.objects.filter(call_id=self.cleaned_data['call_id'], type=pair_type)

        # Verify if we have both start and end calls inside database
        if not pair_call.exists():
            return

        pair_call_objects = {pair_type: pair_call.get(), call.type: call}
        price = PhoneCallPriceCalculator.calculate(pair_call_objects)

        # If price is negative, we assume that invalid data was inserted and don't create the bill for this call
        if price < 0:
            return

        return PhoneBill.objects.create(
            destination=pair_call_objects['start'].destination,
            start_time_stamp=pair_call_objects['start'].time_stamp,
            duration=(pair_call_objects['end'].time_stamp -
                      pair_call_objects['start'].time_stamp).total_seconds(),
            price=price
        )
