from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView

from apps.core.models import Activity
from apps.core.services import PermissionService, visible_activity
from .models import Visit


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "clinic/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["activities"] = visible_activity(self.request.user)
        visit_activity = Activity.objects.filter(slug="visit-board").first()
        visits = Visit.objects.select_related("patient", "patient__owner", "veterinarian").order_by("scheduled_at")
        if not self.request.user.is_superuser:
            visits = PermissionService.filter_queryset(self.request.user, "read", visits, visit_activity)
        context["visits"] = visits[:50]
        context["state_counts"] = {
            state: visits.filter(current_state=state).count()
            for state, _ in Visit.State.choices
        }
        context["now"] = timezone.now()
        return context