from datetime import datetime as dtm
from zoneinfo import ZoneInfo as zi
from django.conf import settings
from django.views.generic import ListView 
from vto_core.models import DemoTestTimestamp


class DemoTestTSList(ListView):
    model = DemoTestTimestamp
    template_name = 'time/demo-ts-list.dtl'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        for obj in context['object_list']:
            xch = dtm.fromtimestamp(obj.ts_unix, tz=zi(obj.exchange.tz.identifier))

            # in addition to the tz middleware converting the utc field in the model
            utc = dtm.fromtimestamp(obj.ts_unix, tz=zi('UTC'))

            # in addition to the tz template tag converting the user tz
            if self.request.user.is_authenticated:
                usr = dtm.fromtimestamp(obj.ts_unix, \
                    tz=zi(str(self.request.user.timezone.identifier)))

        context['ts_xch'] = xch.strftime(settings.TSFMT)
        
        # in addition to the tz middleware converting the utc field in the model
        context['tsv_utc'] = utc.strftime(settings.TSFMT)        

        # in addition to the tz template tag converting the user tz
        if self.request.user.is_authenticated:
            context['tsv_usr'] = usr.strftime(settings.TSFMT)

        return context

'''
            timestamp = obj.ts_unix
            timezone = zi(obj.exchange.tz)
            datetime_object = dtm.fromtimestamp(timestamp, tz=timezone)
            formatted_date = dt.strftime("%Y-%m-%d %H:%M:%S %z %Z")
        context['xch_ts] = formatted_date
'''