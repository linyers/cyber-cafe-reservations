from django import forms
from .models import Device, Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["device"]


class DevicesFilterAdminForm(forms.Form):
    DEVICE_CHOICES = [
        ("device_type", "Device type"),
        ("PC", "PC"),
        ("PS", "PS"),
        ("NINTENDO", "NINTENDO"),
        ("XBOX", "XBOX"),
    ]

    device_type = forms.ChoiceField(
        choices=DEVICE_CHOICES, required=False, label="Device Type"
    )


class ReservationFilterAdminForm(DevicesFilterAdminForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_choice = [("device_name", "Device name")]
        device_names = Device.objects.values_list("name", flat=True).distinct()
        choices = default_choice + [(name, name) for name in device_names]
        self.fields["device_name"] = forms.ChoiceField(
            choices=choices,
            required=False,
            label="Device Name",
        )
