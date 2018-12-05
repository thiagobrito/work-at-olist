from django.db import models

from phone_calls.core.validators import PhoneNumberValidator

'''{
  "id":  // Record unique identificator;
  "type":  // Indicate if it's a call "start" or "end" record;
  "timestamp":  // The timestamp of when the event occured;
  "call_id":  // Unique for each call record pair;
  "source":  // The subscriber phone number that originated the call;
  "destination":  // The phone number receiving the call.
}'''


class PhoneRecord(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField('type', max_length=12)
    time_stamp = models.DateTimeField()
    call_id = models.IntegerField()
    source = models.CharField(max_length=12, validators=[PhoneNumberValidator()])
    destination = models.CharField(max_length=12, validators=[PhoneNumberValidator()])
