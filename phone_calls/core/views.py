from datetime import timedelta, datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from phone_calls.core.forms import BillingForm
from phone_calls.core.models import *
from phone_calls.core.serializers import PhoneBillSerializer, PhoneBillRequestSerializer, PhoneRecordRequestSerializer
from phone_calls.core.services.billing import CreateBilling


class PhoneRecordViewSet(viewsets.ViewSet):
    """
    Saves calling information in the database.
    """

    def create(self, request):
        """
        Saves specific call information inside database.
        """
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

            if data['type'] != 'start' and data['type'] != 'end':
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'error': 'Call type is invalid.'})

            queryset = Call.objects.filter(call_id=data['call_id'], type=data['type'])
            if queryset.exists():
                return Response(status=status.HTTP_400_BAD_REQUEST,
                                data={'error': 'ID and type already exists in database'})

            CreateBilling.execute(billing_form.cleaned_data)

            return Response(data={'call_id': request.data.get('call_id')}, status=status.HTTP_201_CREATED)

        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return PhoneRecordRequestSerializer


class PhoneBillingViewSet(viewsets.ViewSet):
    """
    Retreive billing report from a specific subscriber.
    """

    @action(detail=False, methods=['POST'], name='report')
    def report(self, request, *args, **kwargs):
        """
        Returns all billing information from specific user at period range
        """
        try:
            subscriber = request.data.get('subscriber', None)
            if subscriber is None:
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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

    def get_serializer_class(self):
        return PhoneBillRequestSerializer
