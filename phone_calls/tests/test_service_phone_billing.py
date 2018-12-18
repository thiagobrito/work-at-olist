from decimal import Decimal

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from phone_calls.core.models import Billing
from phone_calls.tests.utils import make_timestamp, make_phone_call


class TestServicePhoneBilling(APITestCase):
    def test_usual_flow_save_bill(self):
        '''Phone call started and some minutes latter. Make sure that the billing is correct'''
        make_phone_call(self.client, time_stamp=make_timestamp(hour=11), type='start')
        make_phone_call(self.client, time_stamp=make_timestamp(hour=12), type='end')
        self.assertTrue(Billing.objects.exists())

    def test_call_fractionated_minute_dont_pay_minute_just_call(self):
        '''We have a call with just one hour inside payable hours'''
        make_phone_call(self.client, make_timestamp(hour=9, minute=0, second=13))
        make_phone_call(self.client, make_timestamp(hour=9, minute=1, second=0), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('0.36'), Billing.objects.get().price)

    def test_only_free_minutes_call_charge_just_for_standing_charge(self):
        '''We have the full call inside free time'''
        make_phone_call(self.client, make_timestamp(hour=23, minute=0, second=13, day=1))
        make_phone_call(self.client, make_timestamp(hour=5, minute=1, second=0, day=2), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('0.36'), Billing.objects.get().price)

    def test_call_free_time_should_calculate_right(self):
        '''We have a call on the free time, let's check if it's calculating correctly'''
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13))
        make_phone_call(self.client, make_timestamp(hour=22, minute=17, second=53), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('0.54'), Billing.objects.get().price)

    def test_call_free_time_should_calculate_right_morning_time_limit_test(self):
        '''This is a trick situation for my algoritm. Let's check if it's calculating morning prices correctly'''
        make_phone_call(self.client, make_timestamp(hour=5, minute=0, second=0))
        make_phone_call(self.client, make_timestamp(hour=6, minute=0, second=0), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('0.36'), Billing.objects.get().price)

    def test_call_free_time_should_calculate_right_morning_time_some_seconds_remaining_limit_test(self):
        '''Let's check if it's calculating morning prices correctly with a fractionated minute'''
        make_phone_call(self.client, make_timestamp(hour=5, minute=0, second=0))
        make_phone_call(self.client, make_timestamp(hour=6, minute=0, second=26), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('0.36'), Billing.objects.get().price)

    def test_call_free_time_should_calculate_right_morning_time_some_minutes_remaining_limit_test(self):
        '''Let's check if it's calculating morning prices correctly with a fractionated minute'''
        make_phone_call(self.client, make_timestamp(hour=5, minute=0, second=0))
        make_phone_call(self.client, make_timestamp(hour=5, minute=59, second=26), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('0.36'), Billing.objects.get().price)

    def test_call_full_free_time_should_calculate_right_limit_test(self):
        '''Start exactly at free time (22h) and finish exactly at free time (next day 6h)'''
        make_phone_call(self.client, make_timestamp(hour=22, minute=0, second=0, day=1))
        make_phone_call(self.client, make_timestamp(hour=6, minute=0, second=0, day=2), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('0.36'), Billing.objects.get().price)

    def test_call_night_free_time_should_calculate_right_limit_test(self):
        '''Start exactly at free time (22h) one hour later, don't charge the minutes'''
        make_phone_call(self.client, make_timestamp(hour=22, minute=0, second=0))
        make_phone_call(self.client, make_timestamp(hour=23, minute=0, second=0), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('0.36'), Billing.objects.get().price)

    def test_call_just_one_hour_normal_time(self):
        '''We have a call with just one hour inside payable hours'''
        make_phone_call(self.client, make_timestamp(hour=9, minute=0, second=0))
        make_phone_call(self.client, make_timestamp(hour=10, minute=0, second=0), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('5.76'), Billing.objects.get().price)

    def test_he_spent_all_night_long_connected(self):
        '''We have a call on the free time, let's check if it's calculating correctly'''
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13, day=1))
        make_phone_call(self.client, make_timestamp(hour=7, minute=17, second=53, day=2), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('7.56'), Billing.objects.get().price)

    def test_five_days_connected_with_payable_minutes(self):
        '''We have a very long connection (5 days), let's check if it's calculating correctly'''
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13, day=1))
        make_phone_call(self.client, make_timestamp(hour=7, minute=17, second=53, day=5), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('266.76'), Billing.objects.get().price)

    def test_five_days_connected_connection_closed_inside_free_time(self):
        '''We have a very long connection (5 days) and the connection was closed at 5'''
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13, day=1))
        make_phone_call(self.client, make_timestamp(hour=5, minute=0, second=0, day=5), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('259.74'), Billing.objects.get().price)

    def test_five_days_connected_connection_closed_before_free_time(self):
        '''We have a very long connection (5 days) and the connection was closed at 5'''
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13, day=1))
        make_phone_call(self.client, make_timestamp(hour=21, minute=0, second=0, day=5), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('340.74'), Billing.objects.get().price)

    def test_five_days_connected_connection_closed_at_night_inside_free_time(self):
        '''We have a very long connection (5 days) and the connection was closed at 5'''
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13, day=1))
        make_phone_call(self.client, make_timestamp(hour=23, minute=0, second=0, day=5), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('346.14'), Billing.objects.get().price)

    def test_five_days_connected_connection_closed_at_night_inside_free_time_more_hours_same_price(self):
        '''We have a very long connection (5 days) and the connection was closed at 5'''
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13, day=1))
        make_phone_call(self.client, make_timestamp(hour=1, minute=0, second=0, day=6), type='end')
        self.assertTrue(Billing.objects.exists())
        self.assertEqual(Decimal('346.14'), Billing.objects.get().price)

    def test_only_start_call_entry__dont_save_bill(self):
        '''We received only start phone call entry. So we don't save anything in the billing yet'''
        make_phone_call(self.client, make_timestamp(hour=12), type='start')
        self.assertFalse(Billing.objects.exists())

    def test_only_end_call_entry__dont_save_bill(self):
        '''We received only end phone call entry. So we don't save anything in the billing yet'''
        make_phone_call(self.client, make_timestamp(hour=12), type='end')
        self.assertFalse(Billing.objects.exists())

    def test_start_call_after_end_call(self):
        '''Well, something wrong happens! We have a start phone call that happened after the end! We ignore this in the phone bill.'''
        make_phone_call(self.client, make_timestamp(hour=22, minute=57, second=13))
        make_phone_call(self.client, make_timestamp(hour=20, minute=0, second=0), type='end')
        self.assertFalse(Billing.objects.exists())

    def test_invalid_timestamp(self):
        '''Well someone inserted a crazy timestamp. We need to identify it and return 400'''
        self.assertEqual(status.HTTP_400_BAD_REQUEST, make_phone_call(self.client, 'invalid').status_code)
        self.assertFalse(Billing.objects.exists())

    def make_test_data(self, **kwargs):
        data = {'destination': '2433263689', 'time_stamp': '2016-02-29T12:00:00Z', 'duration': 60, 'price': 0.32}
        data.update(kwargs)
        return data
