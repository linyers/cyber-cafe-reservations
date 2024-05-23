from django.urls import path, re_path
from .views import (
    index,
    devices_view,
    ReservationView,
    DeviceAdminListView,
    DeviceCreateAdminView,
    DeviceDeleteAdminView,
    DeviceUpdateAdminView,
    ReservationListAdminView,
    ReservationsDeviceTypeAdminView,
    ReservationsDeviceDetailAdminView,
    ReservationDeleteAdminView,
)

app_name = "cyber"

urlpatterns = [
    path("", index, name="index"),
    path("devices/", devices_view, name="devices"),
    re_path(
        r"(?P<device>pc|ps|xbox|nintendo)/reservation/",
        ReservationView.as_view(),
        name="reservation",
    ),
    path("devices/list/", DeviceAdminListView.as_view(), name="device-list"),
    path("devices/create/", DeviceCreateAdminView.as_view(), name="device-create"),
    path("update/<int:pk>/", DeviceUpdateAdminView.as_view(), name="device-update"),
    path("delete/<int:pk>/", DeviceDeleteAdminView.as_view(), name="device-delete"),
    path(
        "reservations/list/",
        ReservationListAdminView.as_view(),
        name="reservation-list",
    ),
    re_path(
        r"reservations/type/(?P<device>pc|ps|xbox|nintendo)/",
        ReservationsDeviceTypeAdminView.as_view(),
        name="reservations-device-type-admin",
    ),
    path(
        "reservations/device/<int:device_id>/",
        ReservationsDeviceDetailAdminView.as_view(),
        name="reservations-device-detail-admin",
    ),
    path(
        "reservations/delete/<int:pk>/",
        ReservationDeleteAdminView.as_view(),
        name="reservation-delete-admin",
    ),
]
