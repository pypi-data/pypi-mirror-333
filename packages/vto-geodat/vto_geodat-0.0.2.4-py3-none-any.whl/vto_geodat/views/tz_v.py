from django.views.generic import ListView 

# from vto_geodat.models import TZAbbreviation
from vto_geodat.models import TimeZone

class TZList(ListView):
    model = TimeZone
    template_name = 'geodat/tz_list.dtl'