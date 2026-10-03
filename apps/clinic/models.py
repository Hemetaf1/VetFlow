from django.conf import settings
from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=160)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    class Species(models.TextChoices):
        DOG = "DOG", "Dog"
        CAT = "CAT", "Cat"
        OTHER = "OTHER", "Other"

    name = models.CharField(max_length=120)
    species = models.CharField(max_length=8, choices=Species.choices, default=Species.DOG)
    breed = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name="patients")

    def __str__(self):
        return self.name


class Visit(models.Model):
    class State(models.TextChoices):
        BOOKED = "BOOKED", "Booked"
        CHECK_IN = "CHECK_IN", "Checked in"
        TRIAGE = "TRIAGE", "Triage"
        IN_EXAM = "IN_EXAM", "In examination"
        PROCEDURE = "PROCEDURE", "Procedure"
        RECOVERY = "RECOVERY", "Recovery"
        DISCHARGE = "DISCHARGE", "Discharge"
        BILLED = "BILLED", "Billed"

    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="visits")
    branch = models.CharField(max_length=120, default="Main clinic")
    veterinarian = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="vet_visits")
    scheduled_at = models.DateTimeField()
    current_state = models.CharField(max_length=20, choices=State.choices, default=State.BOOKED)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_at"]

    def __str__(self):
        return f"{self.patient} visit"


class Procedure(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE, related_name="procedures")
    name = models.CharField(max_length=160)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProcedureSession(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, related_name="sessions")
    starts_at = models.DateTimeField()
    planned_minutes = models.PositiveSmallIntegerField(default=30)
    actual_end = models.DateTimeField(null=True, blank=True)
    is_complete = models.BooleanField(default=False)
    vet_confirmed_completion = models.BooleanField(default=False)
    staff = models.ManyToManyField("staffing.Staff", through="resources.ResourceAllocate", related_name="sessions", blank=True)

    @property
    def planned_end(self):
        from datetime import timedelta
        return self.starts_at + timedelta(minutes=self.planned_minutes)

    def __str__(self):
        return f"{self.procedure} session"