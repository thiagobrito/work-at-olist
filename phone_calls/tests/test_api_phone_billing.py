from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status

from phone_calls.tests.utils import make_phone_call, make_timestamp
from phone_calls.core.views import PhoneBillingViewSet


class TestApiPhoneRecord(APITestCase):
    def setUp(self):
        make_phone_call(self.client, make_timestamp(hour=21, minute=57, second=13))
        make_phone_call(self.client, make_timestamp(hour=22, minute=17, second=53), type='end')
        self.view = PhoneBillingViewSet.as_view({'post': 'report'})

    def test_only_found_subscriber(self):
        request = APIRequestFactory().post('', data={'subscriber': '5512345678'})
        response = self.view(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertDictEqual({
            "id": 1,
            "subscriber": "5512345678",
            "time_stamp": {"start_time": "21:57:13", "start_date": "29/02/2016"},
            "duration": "00h20m40s",
            "price": "R$ 0.54"
        }, dict(response.data[0]))

    def test_subscriber_not_found(self):
        request = APIRequestFactory().post('', data={'subscriber': 'not.found'})
        response = self.view(request)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)
