from django.urls import path, re_path
from .views import index, devices, ReservationView

app_name = "cyber"

urlpatterns = [
    path("", index, name="index"),
    path("devices/", devices, name="devices"),
    re_path(
        r"(?P<device>pc|ps|xbox|nintendo)/reservation/",
        ReservationView.as_view(),
        name="reservation",
    ),
]
