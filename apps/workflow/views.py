import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from apps.clinic.models import Visit
from apps.core.models import Activity
from apps.core.services import PermissionService
from .services import TransitionNotAllowedError, WorkflowService


class WorkflowTransitionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            visit = Visit.objects.get(pk=pk)
            activity = Activity.objects.filter(slug="visit-board").first()
            if not PermissionService.can(request.user, "update", visit, activity=activity):
                return JsonResponse({"error": "You do not have permission to update this visit."}, status=403)
            payload = json.loads(request.body or "{}")
            if not isinstance(payload, dict):
                return JsonResponse({"error": "The request body must be a JSON object."}, status=400)
            WorkflowService.transition(visit, payload.get("to_state", ""), request.user)
        except Visit.DoesNotExist:
            return JsonResponse({"error": "Visit not found."}, status=404)
        except (json.JSONDecodeError, TypeError):
            return JsonResponse({"error": "Invalid JSON request."}, status=400)
        except TransitionNotAllowedError as error:
            return JsonResponse({"error": str(error)}, status=400)
        return JsonResponse({"id": visit.pk, "state": visit.current_state})