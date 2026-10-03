from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from apps.clinic.models import Owner, Patient, Visit, Procedure, ProcedureSession
from apps.workflow.models import StateNavigation
from apps.workflow.services import TransitionNotAllowedError, WorkflowService


class WorkflowServiceTests(TestCase):
    def setUp(self):
        self.owner = Owner.objects.create(name="Jordan Lee")
        self.patient = Patient.objects.create(name="Miso", owner=self.owner)
        self.visit = Visit.objects.create(patient=self.patient, scheduled_at=timezone.now())

    def test_allowed_transition_updates_visit(self):
        StateNavigation.objects.create(model_label="clinic.visit", from_state="BOOKED", to_state="CHECK_IN", label="Check in")

        WorkflowService.transition(self.visit, "CHECK_IN", User.objects.create_user(username="nurse"))

        self.visit.refresh_from_db()
        self.assertEqual(self.visit.current_state, "CHECK_IN")

    def test_transition_is_rejected_when_requirement_fails(self):
        procedure = Procedure.objects.create(visit=self.visit, name="X-ray")
        ProcedureSession.objects.create(procedure=procedure, starts_at=timezone.now())
        StateNavigation.objects.create(
            model_label="clinic.visit", from_state="BOOKED", to_state="DISCHARGE",
            label="Discharge", condition={"type": "no_open_sessions"},
        )

        with self.assertRaises(TransitionNotAllowedError):
            WorkflowService.transition(self.visit, "DISCHARGE")

    def test_unknown_transition_is_rejected(self):
        with self.assertRaises(TransitionNotAllowedError):
            WorkflowService.transition(self.visit, "DISCHARGE")