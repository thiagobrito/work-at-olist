from django import forms

from phone_calls.core.validators import phone_number_validator


class BillingForm(forms.Form):
    type = forms.CharField()
    time_stamp = forms.DateTimeField()
    call_id = forms.IntegerField()
    source = forms.CharField(validators=[phone_number_validator])
    destination = forms.CharField(validators=[phone_number_validator])
