import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response

from phone_calls.core.models import *
from phone_calls.core.serializers import PhoneBillSerializer
from phone_calls.core.services import InvalidInputsError
from phone_calls.core.services.billing import CreateBilling


class PhoneRecordViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            time_stamp = datetime.datetime.strptime(request.data.get('time_stamp'), '%Y-%m-%dT%H:%M:%SZ')

            CreateBilling.execute({
                'type': request.data.get('type'),
                'time_stamp': time_stamp,
                'call_id': request.data.get('call_id'),
                'source': request.data.get('source'),
                'destination': request.data.get('destination')
            })
            return Response(status=status.HTTP_201_CREATED)

        except InvalidInputsError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PhoneBillingViewSet(viewsets.ModelViewSet):
    queryset = PhoneBill.objects.all()
    serializer_class = PhoneBillSerializer
