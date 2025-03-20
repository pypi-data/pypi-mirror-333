from django.urls import path
from .views import TZList

urlpatterns = [
    path('core/iana-zone-list/', TZList.as_view(), name='tz_list'),
]