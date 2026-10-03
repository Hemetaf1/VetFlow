from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.utils import timezone

from apps.clinic.models import Owner, Patient, Visit
from .models import Activity, CRUDPermission, OrganisationChart
from .services import PermissionService


class PermissionServiceTests(TestCase):
    def setUp(self):
        self.parent_group = Group.objects.create(name="Clinic managers")
        self.branch_group = Group.objects.create(name="North branch")
        self.parent_node = OrganisationChart.objects.create(name="Clinic", group=self.parent_group)
        self.branch_node = OrganisationChart.objects.create(
            name="North", group=self.branch_group, parent=self.parent_node,
        )
        self.activity = Activity.objects.create(name="Visit board", slug="visit-board")
        self.user = User.objects.create_user(username="vet")
        self.user.groups.add(self.branch_group)
        self.owner = Owner.objects.create(name="Jordan Lee")
        self.patient = Patient.objects.create(name="Miso", owner=self.owner)
        self.visit = Visit.objects.create(
            patient=self.patient, veterinarian=self.user, scheduled_at=timezone.now(), current_state="TRIAGE",
        )
        CRUDPermission.objects.create(
            activity=self.activity,
            organisation=self.parent_node,
            can_read=True,
            states=["TRIAGE"],
            row_condition={"field": "veterinarian__username", "op": "eq", "value": "$current_user"},
        )

    def test_inherits_parent_permission_and_applies_row_condition(self):
        self.assertTrue(PermissionService.can(self.user, "read", self.visit, self.activity))
        self.assertEqual(
            list(PermissionService.filter_queryset(self.user, "read", Visit.objects.all(), self.activity)),
            [self.visit],
        )

    def test_does_not_grant_access_outside_configured_state_or_row(self):
        self.visit.current_state = "BOOKED"
        self.visit.save(update_fields=["current_state"])
        self.assertFalse(PermissionService.can(self.user, "read", self.visit, self.activity))

        self.visit.current_state = "TRIAGE"
        self.visit.veterinarian = None
        self.visit.save(update_fields=["current_state", "veterinarian"])
        self.assertFalse(PermissionService.can(self.user, "read", self.visit, self.activity))