from django.urls import path
from vto_time.views import TZList

urlpatterns = [
    path('time/iana-zone-list/', TZList.as_view(), name='tz_list'),
]