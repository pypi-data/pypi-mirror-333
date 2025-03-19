from django.urls import path
from vto_geodat.views import TZList

urlpatterns = [
    path("tzl/", TZList.as_view(), name="tz_list"),
]