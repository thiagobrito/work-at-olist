from django.urls import path, include
from rest_framework import routers

import phone_calls.core.views

router = routers.DefaultRouter()
router.register(r'phone_record', phone_calls.core.views.PhoneRecordViewSet, 'phone_record')
router.register(r'phone_bill', phone_calls.core.views.PhoneBillingViewSet, 'phone_billing')

urlpatterns = [
    path(r'', include(router.urls)),
]
