from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta

from .models import Device, Reservation
from .forms import DevicesFilterAdminForm, ReservationFilterAdminForm, ReservationForm


def index(request):
    user = request.user
    return render(request, "index.html", {"user": user})


def devices_view(request):
    return render(request, "devices.html")


class ReservationView(TemplateView):
    devices = {
        "PC": "PC",
        "PS": "PlayStation",
        "XBOX": "Xbox",
        "NINTENDO": "Nintendo Switch",
    }

    def get(self, request, device):
        device = device.upper()

        hours = request.GET.get("hours")
        started_at = request.GET.get("started_at")

        if not hours or not started_at:
            return render(
                request, "reservation_search.html", {"device": self.devices[device]}
            )

        start_time = datetime.strptime(started_at, "%Y-%m-%dT%H:%M")
        end_time = start_time + timedelta(hours=int(hours))

        available_devices = Device.objects.find_available_devices(
            start_time, end_time, device
        )

        return render(
            request,
            "reservation.html",
            {
                "device": self.devices[device],
                "hours": hours,
                "start_time": started_at,
                "end_time": end_time,
                "available_devices": available_devices,
            },
        )

    @method_decorator(login_required)
    def post(self, request, device):
        device = device.upper()

        hours = request.GET.get("hours")
        started_at = request.GET.get("started_at")
        start_time = datetime.strptime(started_at, "%Y-%m-%dT%H:%M")
        end_time = start_time + timedelta(hours=int(hours))

        available_devices = Device.objects.find_available_devices(
            start_time, end_time, device
        )

        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            selected_device = request.POST["device"]

            reservation.device = Device.objects.get(pk=selected_device)
            reservation.start_time = start_time
            reservation.end_time = end_time

            user = request.user
            reservation.user = user

            reservation.save()

            return redirect("cyber:index")

        return render(
            request,
            "reservation.html",
            {
                "device": self.devices[device],
                "hours": hours,
                "start_time": start_time,
                "end_time": end_time,
                "available_devices": available_devices,
            },
        )


class DeviceAdminListView(UserPassesTestMixin, ListView):
    model = Device
    template_name = "device_list.html"
    context_object_name = "devices"

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        queryset = super().get_queryset()
        form = DevicesFilterAdminForm(self.request.GET or None)

        if not form.is_valid():
            return queryset

        if form.cleaned_data["device_type"] != "device_type":
            queryset = queryset.filter(device_type=form.cleaned_data["device_type"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = DevicesFilterAdminForm(self.request.GET or None)
        return context


class DeviceCreateAdminView(UserPassesTestMixin, CreateView):
    model = Device
    template_name = "device_form.html"
    fields = ["name", "image", "device_type"]
    success_url = reverse_lazy("cyber:devices-list")

    def test_func(self):
        return self.request.user.is_superuser


class DeviceUpdateAdminView(UserPassesTestMixin, UpdateView):
    model = Device
    template_name = "device_form.html"
    fields = ["name", "image", "device_type"]
    success_url = reverse_lazy("cyber:device-list")

    def test_func(self):
        return self.request.user.is_superuser


class DeviceDeleteAdminView(UserPassesTestMixin, DeleteView):
    model = Device
    template_name = "device_confirm_delete.html"
    success_url = reverse_lazy("cyber:device-list")

    def test_func(self):
        return self.request.user.is_superuser


class ReservationListAdminView(UserPassesTestMixin, ListView):
    model = Reservation
    template_name = "reservation_list.html"
    context_object_name = "reservations"

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ReservationFilterAdminForm(self.request.GET or None)

        if not form.is_valid():
            return queryset

        if form.cleaned_data["device_name"] != "device_name":
            queryset = queryset.filter(device__name=form.cleaned_data["device_name"])
        if form.cleaned_data["device_type"] != "device_type":
            queryset = queryset.filter(
                device__device_type=form.cleaned_data["device_type"]
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReservationFilterAdminForm(self.request.GET or None)
        return context


class ReservationDeleteAdminView(UserPassesTestMixin, DeleteView):
    model = Reservation
    template_name = "reservation_confirm_delete.html"
    context_object_name = "reservation"

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        next_url = self.request.GET.get("next", reverse_lazy("cyber:reservation-list"))
        return next_url

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return redirect(self.get_success_url())
