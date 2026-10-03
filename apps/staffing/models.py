from django.conf import settings
from django.db import models


class Staff(models.Model):
    class Role(models.TextChoices):
        VETERINARIAN = "VETERINARIAN", "Veterinarian"
        NURSE = "NURSE", "Nurse"
        RECEPTION = "RECEPTION", "Reception"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile")
    role = models.CharField(max_length=20, choices=Role.choices)
    branch = models.CharField(max_length=120, default="Main clinic")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


class Shift(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="shifts")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()


class StaffAvailability(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="availability_windows")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    reason = models.CharField(max_length=160)