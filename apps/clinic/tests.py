from django.contrib.auth.models import User
from django.test import TestCase


class DashboardTests(TestCase):
    def test_authenticated_superuser_can_open_dashboard(self):
        admin = User.objects.create_superuser(username="clinic-admin", password="test-password")
        self.client.force_login(admin)

        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visit board")
        self.assertContains(response, "Administration")