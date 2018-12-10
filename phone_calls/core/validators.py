from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

'''
The phone number format is AAXXXXXXXXX, where AA is the area code and XXXXXXXXX is the phone number.
The area code is always composed of two digits while the phone number can be composed of 8 or 9 digits.
'''


def phone_number_validator(value):
    message = _(
        'Ensure the phone number is with valid format The phone number format is AAXXXXXXXXX, where AA is the area code and XXXXXXXXX is the phone number. The area code is always composed of two digits while the phone number can be composed of 8 or 9 digits.')
    code = 'phone'

    if not value.isnumeric():
        raise ValidationError(message, code=code)

    if len(value) != 10 and len(value) != 11:
        raise ValidationError(message, code=code)


def price_validator(value):
    if value < 0:
        raise ValidationError('Price is negative. Probably the start call is marked after end call', code='value')
