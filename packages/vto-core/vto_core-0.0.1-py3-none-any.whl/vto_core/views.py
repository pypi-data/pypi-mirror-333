from django.views.generic import ListView 
from .models import TimeZone

class TZList(ListView):
    model = TimeZone
    template_name = 'time/tz_list.dtl'