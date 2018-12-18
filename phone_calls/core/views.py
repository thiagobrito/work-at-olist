from datetime import timedelta, datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from phone_calls.core.forms import BillingForm
from phone_calls.core.models import *
from phone_calls.core.serializers import PhoneBillSerializer, PhoneRecordSerializer
from phone_calls.core.services.billing import CreateBilling


class PhoneRecordViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            time_stamp = datetime.strptime(request.data.get('time_stamp'), '%Y-%m-%dT%H:%M:%SZ')
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


class PhoneBillingViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['post'])
    def report(self, request):
        try:
            subscriber = request.data.get('subscriber', None)

            period = request.data.get('period', None)
            if period:
                d = datetime.strptime(period, '%m-%Y')
            else:
                # Period not informed, we'll use the last month
                d = datetime.now().replace(day=1) - timedelta(days=1)

            queryset = Billing.objects.filter(subscriber=subscriber,
                                              start_time_stamp__year=d.year, start_time_stamp__month=d.month)
            serializer = PhoneBillSerializer(queryset, many=True)
            return Response(serializer.data)

        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
