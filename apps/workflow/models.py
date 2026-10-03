from django.db import models


class StateInTable(models.Model):
    model_label = models.CharField(max_length=100, help_text="Django model label, for example clinic.Visit")
    state = models.CharField(max_length=40)
    display_name = models.CharField(max_length=80)

    class Meta:
        unique_together = [("model_label", "state")]
        ordering = ["model_label", "state"]

    def __str__(self):
        return f"{self.model_label}: {self.display_name}"


class StateNavigation(models.Model):
    model_label = models.CharField(max_length=100, default="clinic.visit")
    from_state = models.CharField(max_length=40)
    to_state = models.CharField(max_length=40)
    label = models.CharField(max_length=80)
    condition = models.JSONField(default=dict, blank=True)
    action = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [("model_label", "from_state", "to_state")]

    def __str__(self):
        return f"{self.from_state} -> {self.to_state}"