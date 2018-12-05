from django.test import TestCase

from phone_calls.core.validators import *


class PhoneNumberValidatorTests(TestCase):
    def setUp(self):
        self.validator = PhoneNumberValidator()

    def test_not_a_number_raise_exception(self):
        with self.assertRaises(ValidationError):
            self.validator('test')

    def test_invalid_number(self):
        with self.assertRaises(ValidationError):
            self.validator('123')

    def test_big_number(self):
        with self.assertRaises(ValidationError):
            self.validator('5533333333355')

    def test_eight_valid_number(self):
        self.validator('5512345678')

    def test_nine_valid_number(self):
        self.validator('55123456789')
