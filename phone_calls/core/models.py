from django.db import models

from phone_calls.core.validators import phone_number_validator


class Call(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField('type', max_length=12)
    time_stamp = models.DateTimeField()
    call_id = models.IntegerField()
    source = models.CharField(max_length=12, validators=[phone_number_validator])
    destination = models.CharField(max_length=12, validators=[phone_number_validator])


class Billing(models.Model):
    id = models.AutoField(primary_key=True)
    destination = models.CharField(max_length=12, validators=[phone_number_validator])
    start_time_stamp = models.DateTimeField()
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
