from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=120, default="Main clinic")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=120)
    branch = models.CharField(max_length=120, default="Main clinic")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ResourceAllocate(models.Model):
    session = models.ForeignKey("clinic.ProcedureSession", on_delete=models.CASCADE, related_name="allocations")
    staff = models.ForeignKey("staffing.Staff", null=True, blank=True, on_delete=models.PROTECT)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.PROTECT)
    equipment = models.ForeignKey(Equipment, null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["session", "staff"], name="unique_session_staff_allocation")]