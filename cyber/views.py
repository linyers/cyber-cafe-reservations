from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from datetime import datetime, timedelta

from .models import Device, Reservation
from .forms import ReservationForm


def index(request):
    user = request.user
    return render(request, "index.html", {"user": user})


def devices(request):
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
