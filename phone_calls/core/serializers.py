from rest_framework import serializers

from phone_calls.core.fields import MoneyBrlField, DurationField, SeparatedDateTimeFields
from phone_calls.core.models import PhoneRecord, PhoneBill


class PhoneRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhoneRecord
        fields = ('id', 'type', 'time_stamp', 'call_id', 'source', 'destination')


class PhoneBillSerializer(serializers.HyperlinkedModelSerializer):
    price = MoneyBrlField(label='Price')
    duration = DurationField(label='Duration')
    time_stamp = SeparatedDateTimeFields(source='start_time_stamp')

    class Meta:
        model = PhoneBill
        fields = ('id', 'destination', 'time_stamp', 'duration', 'price')
