from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from phone_calls.tests.utils import make_phone_call, make_timestamp, previous_month_date
from phone_calls.core.views import PhoneBillingViewSet


class TestApiPhoneRecord(APITestCase):
    def setUp(self):
        date = previous_month_date(False)
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13,
                                                    day=date.day, month=date.month, year=date.year))
        make_phone_call(self.client, make_timestamp(hour=22, minute=17, second=53,
                                                    day=date.day, month=date.month, year=date.year), type='end')
        self.view = PhoneBillingViewSet.as_view({'post': 'report'})

    def test_existent_subscriber_period_not_informed(self):
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13, year=2017), call_id=71)
        make_phone_call(self.client, make_timestamp(hour=22, minute=17, second=53, year=2017), call_id=71, type='end')

        request = APIRequestFactory().post('', data={'subscriber': '5512345678'})
        response = self.view(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictEqual({
            "id": 1,
            "subscriber": "5512345678",
            "time_stamp": {"start_time": "21:57:13", "start_date": previous_month_date()},
            "duration": "00h20m40s",
            "price": "R$ 0.54"
        }, dict(response.data[0]))

    def test_subscriber_not_found(self):
        request = APIRequestFactory().post('', data={'subscriber': 'not.found'})
        response = self.view(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)

    def test_existent_period(self):
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13, year=2017), call_id=71)
        make_phone_call(self.client, make_timestamp(hour=22, minute=17, second=53, year=2017), call_id=71, type='end')

        date = previous_month_date(False)
        request = APIRequestFactory().post('', data={'subscriber': '5512345678',
                                                     'period': '%d-%d' % (date.month, date.year)})
        response = self.view(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertDictEqual({
            "id": 1,
            "subscriber": "5512345678",
            "time_stamp": {"start_time": "21:57:13", "start_date": previous_month_date()},
            "duration": "00h20m40s",
            "price": "R$ 0.54"
        }, dict(response.data[0]))

    def test_period_not_found(self):
        request = APIRequestFactory().post('', data={'subscriber': '5512345678', 'period': '10-2018'})
        response = self.view(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(0, len(response.data))

    def test_period_invalid_return_invalid_request(self):
        request = APIRequestFactory().post('', data={'subscriber': '5512345678', 'period': 'INVALID.PERIOD'})
        response = self.view(request)

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
