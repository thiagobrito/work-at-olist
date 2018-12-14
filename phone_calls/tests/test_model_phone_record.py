from django.core.exceptions import ValidationError
from django.test import TestCase

from phone_calls.core.models import Call


class PhoneRecordTests(TestCase):
    def test_valid_numbers_record_should_create(self):
        Call.objects.create(id=234, type='start', time_stamp='2016-02-29T12:00:00Z',
                            call_id=70, source='5512345678', destination='44123456789')
        self.assertTrue(Call.objects.exists())

    def test_invalid_number_source(self):
        phone_record = Call.objects.create(id=123, type='start', time_stamp='2016-02-29T12:00:00Z',
                                           call_id=70, source='invalid', destination='55123456789')
        self.assertRaises(ValidationError, phone_record.full_clean)

    def test_invalid_number_destination(self):
        phone_record = Call.objects.create(id=123, type='start', time_stamp='2016-02-29T12:00:00Z',
                                           call_id=70, source='55123456789', destination='invalid')
        self.assertRaises(ValidationError, phone_record.full_clean)
