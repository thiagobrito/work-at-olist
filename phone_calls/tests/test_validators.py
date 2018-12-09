from django.test import TestCase

from phone_calls.core.validators import *


class PhoneNumberValidatorTests(TestCase):
    def test_not_a_number_raise_exception(self):
        with self.assertRaises(ValidationError):
            phone_number_validator('test')

    def test_invalid_number(self):
        with self.assertRaises(ValidationError):
            phone_number_validator('123')

    def test_big_number(self):
        with self.assertRaises(ValidationError):
            phone_number_validator('5533333333355')

    def test_eight_valid_number(self):
        phone_number_validator('5512345678')

    def test_nine_valid_number(self):
        phone_number_validator('55123456789')
