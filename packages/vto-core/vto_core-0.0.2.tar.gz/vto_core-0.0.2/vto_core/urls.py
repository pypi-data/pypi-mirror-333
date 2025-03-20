from django.urls import path
from vto_core.views import TZList, DemoTestTSList

urlpatterns = [
    path('core/iana-tz-list/', TZList.as_view(), name='tz_list'),
    path('core/demo-ts-render/', DemoTestTSList.as_view(), name='demo_ts_render'),
]