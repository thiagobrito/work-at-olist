from rest_framework import serializers, viewsets

from phone_calls.core.models import *


class PhoneRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PhoneRecord
        fields = ('id', 'type', 'time_stamp', 'call_id', 'source', 'destination')


class PhoneRecordViewSet(viewsets.ModelViewSet):
    queryset = PhoneRecord.objects.all()
    serializer_class = PhoneRecordSerializer
