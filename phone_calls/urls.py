from django.urls import path, include
from rest_framework import routers
from rest_framework_docs.views import DRFDocsView

import phone_calls.core.views

router = routers.DefaultRouter()
router.register(r'phone_record', phone_calls.core.views.PhoneRecordViewSet, 'phone_record')
router.register(r'phone_billing', phone_calls.core.views.PhoneBillingViewSet, 'phone_billing')


def docs():
    drf_docs = DRFDocsView
    drf_docs.drf_router = router
    return drf_docs.as_view()


urlpatterns = [
    path(r'', docs(), name='drfdocs'),
    path(r'', include(router.urls)),
]
