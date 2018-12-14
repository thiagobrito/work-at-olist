from rest_framework.reverse import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from phone_calls.core.models import Call


class TestApiPhoneRecord(APITestCase):
    def test_insert_valid_data(self):
        response = self.client.post(reverse('phone_record-list'), self.make_test_data(), format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Call.objects.count())
        self.assertEqual(1, Call.objects.get().id)

    def test_insert_invalid_phone_number(self):
        data = self.make_test_data(source='aaa', destination='bbb')
        response = self.client.post(reverse('phone_record-list'), data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(0, Call.objects.count())

    def make_test_data(self, **kwargs):
        data = {'type': 'start', 'time_stamp': '2016-02-29T12:00:00Z',
                'call_id': 70, 'source': '5512345678', 'destination': '44123456789'}
        data.update(kwargs)
        return data
