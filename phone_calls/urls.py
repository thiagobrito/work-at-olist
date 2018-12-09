from django.urls import path, include
from rest_framework import routers

import phone_calls.core.views

router = routers.DefaultRouter()
router.register(r'phone_record', phone_calls.core.views.PhoneRecordViewSet, 'phone_record')

urlpatterns = [
    path(r'', include(router.urls)),
]
