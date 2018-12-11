from rest_framework import viewsets

from phone_calls.core.models import *
from phone_calls.core.serializers import PhoneRecordSerializer, PhoneBillSerializer


class PhoneRecordViewSet(viewsets.ModelViewSet):
    queryset = PhoneRecord.objects.all()
    serializer_class = PhoneRecordSerializer


class PhoneBillingViewSet(viewsets.ModelViewSet):
    queryset = PhoneBill.objects.all()
    serializer_class = PhoneBillSerializer
