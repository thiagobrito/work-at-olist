from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from phone_calls.core.models import PhoneBill


class TestApiPhoneRecord(APITestCase):
    def test_insert_valid_data(self):
        response = self.client.post(reverse('phone_billing-list'), self.make_test_data(), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, PhoneBill.objects.count())
        self.assertEqual(1, PhoneBill.objects.get().id)

    def make_test_data(self, **kwargs):
        data = {'destination': '2433263689', 'time_stamp': '2016-02-29T12:00:00Z', 'duration': 60, 'price': 0.32}
        data.update(kwargs)
        return data
