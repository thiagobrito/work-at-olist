from phone_calls.core.services import Service
from phone_calls.core.models import *
from phone_calls.core.price import *


class CreateBilling(Service):
    def process(self):
        call = Call.objects.create(**self.cleaned_data)
        self._save_billing_report(call)
        return call

    def _save_billing_report(self, call):
        pair_type = 'end' if call.type == 'start' else 'start'
        pair_call = Call.objects.filter(call_id=self.cleaned_data['call_id'], type=pair_type)

        # Verify if we have both start and end calls inside database
        if not pair_call.exists():
            return

        pair_call_objects = {pair_type: pair_call.get(), call.type: call}
        call_period = Period(pair_call_objects['start'].time_stamp, pair_call_objects['end'].time_stamp)
        price = PhoneCallPriceCalculator.calculate(call_period)

        # If price is negative, we assume that an invalid data was inserted and don't create the bill for this call
        if price < 0:
            return

        return Billing.objects.create(
            subscriber=pair_call_objects['start'].source,
            start_time_stamp=call_period.start,
            duration=call_period.seconds_diff(),
            price=price
        )
