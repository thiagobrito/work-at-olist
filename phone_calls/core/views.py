import datetime

from rest_framework import viewsets, status
from rest_framework.response import Response

from phone_calls.core.forms import BillingForm
from phone_calls.core.models import *
from phone_calls.core.serializers import PhoneBillSerializer
from phone_calls.core.services.billing import CreateBilling


class PhoneRecordViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            time_stamp = datetime.datetime.strptime(request.data.get('time_stamp'), '%Y-%m-%dT%H:%M:%SZ')
            data = {
                'type': request.data.get('type'),
                'time_stamp': time_stamp,
                'call_id': request.data.get('call_id'),
                'source': request.data.get('source'),
                'destination': request.data.get('destination')
            }

            billing_form = BillingForm(data)
            if not billing_form.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            CreateBilling.execute(billing_form.cleaned_data)

            return Response(status=status.HTTP_201_CREATED)

        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PhoneBillingViewSet(viewsets.ModelViewSet):
    queryset = Billing.objects.all()
    serializer_class = PhoneBillSerializer
