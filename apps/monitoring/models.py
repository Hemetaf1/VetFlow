from django.db import models


class UnpredictedEvent(models.Model):
    class Category(models.TextChoices):
        EMERGENCY = "EMERGENCY", "Emergency arrival"
        ABSENCE = "ABSENCE", "Staff absence"
        EQUIPMENT = "EQUIPMENT", "Equipment failure"
        OVERRUN = "OVERRUN", "Procedure overrun"

    category = models.CharField(max_length=20, choices=Category.choices)
    occurred_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    related_session = models.ForeignKey("clinic.ProcedureSession", null=True, blank=True, on_delete=models.SET_NULL)
    handled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-occurred_at"]