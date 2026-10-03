from django.core.exceptions import FieldDoesNotExist
from django.db import transaction

from .models import StateNavigation


class TransitionNotAllowedError(Exception):
    pass


class WorkflowService:
    @classmethod
    @transaction.atomic
    def transition(cls, instance, target_state, user=None):
        model_label = instance._meta.label_lower
        navigation = StateNavigation.objects.select_for_update().filter(
            model_label=model_label, from_state=instance.current_state,
            to_state=target_state, is_active=True,
        ).first()
        if navigation is None:
            raise TransitionNotAllowedError("This transition is not allowed.")
        if not cls._condition_passes(navigation.condition, instance):
            raise TransitionNotAllowedError("The visit cannot move because its requirements are not met.")
        instance.current_state = target_state
        instance.save(update_fields=["current_state", "updated_at"])
        return instance

    @staticmethod
    def _condition_passes(condition, instance):
        if not condition:
            return True
        if condition.get("type") == "no_open_sessions":
            return not instance.procedures.filter(sessions__is_complete=False).exists()
        field = condition.get("field")
        if not field or condition.get("op") not in {"eq", "ne"}:
            return False
        try:
            instance._meta.get_field(field)
        except FieldDoesNotExist:
            return False
        actual = getattr(instance, field)
        expected = condition.get("value")
        return (actual == expected) if condition["op"] == "eq" else (actual != expected)