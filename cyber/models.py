from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete


class DeviceManager(models.Manager):
    def find_available_devices(self, start_time, end_time, device) -> list:
        not_available_device_ids = Reservation.objects.filter(
            device__device_type=device,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).values_list("device_id", flat=True)

        available_devices = Device.objects.filter(device_type=device).exclude(
            id__in=not_available_device_ids
        )

        return available_devices


class Device(models.Model):
    DEVICE_TYPES = [
        ("PC", "PC"),
        ("PS", "PlayStation"),
        ("XBOX", "Xbox"),
        ("NINTENDO", "Nintendo"),
    ]
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="device_images/", blank=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES)
    available = models.BooleanField(default=True)  # Change

    objects = DeviceManager()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Reservation of {self.device.name} by {self.user.username} from {self.start_time} to {self.end_time}"

    def save(self, *args, **kwargs):
        overlapping_reservations = Reservation.objects.filter(
            device=self.device,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )
        if overlapping_reservations.exists():
            raise ValueError(
                "This device is already reserved for the given time period."
            )
        super().save(*args, **kwargs)


def set_name(sender, instance, *args, **kwargs):
    if instance.name:
        return

    device_count = Device.objects.filter(device_type=instance.device_type).count()
    instance.name = f"{instance.device_type} {device_count + 1}"


def set_image(sender, instance, *args, **kwargs):
    if instance.image:
        return

    images = {
        "PC": "default_images/pc_default.png",
        "PS": "default_images/ps_default.png",
        "XBOX": "default_images/xbox_default.png",
        "Nintendo": "default_images/nintendo_default.png",
    }
    instance.image = images[instance.device_type]


def set_all_devices_name(sender, instance, *args, **kwargs):
    devices = Device.objects.filter(device_type=instance.device_type)
    for index, device in enumerate(devices):
        device.name = f"{device.device_type} {index + 1}"
    Device.objects.bulk_update(devices, ["name"])


pre_save.connect(set_name, sender=Device)
pre_save.connect(set_image, sender=Device)
post_delete.connect(set_all_devices_name, sender=Device)
