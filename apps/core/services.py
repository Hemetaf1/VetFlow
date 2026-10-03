from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q

from .models import Activity, CRUDPermission, OrganisationChart


class PermissionService:
    ACTION_FIELDS = {"create": "can_create", "read": "can_read", "update": "can_update", "delete": "can_delete"}

    @classmethod
    def can(cls, user, action, obj=None, activity=None):
        if not user.is_authenticated or action not in cls.ACTION_FIELDS:
            return False
        if activity is None:
            return False
        if user.is_superuser:
            return True
        if obj is not None:
            return cls.filter_queryset(user, action, type(obj).objects.filter(pk=obj.pk), activity).exists()
        return cls._permissions(user, action, activity).exists()

    @classmethod
    def filter_queryset(cls, user, action, queryset, activity):
        if not user.is_authenticated or action not in cls.ACTION_FIELDS or activity is None:
            return queryset.none()
        if user.is_superuser:
            return queryset
        allowed = Q(pk__in=[])
        for permission in cls._permissions(user, action, activity):
            rule = Q()
            if permission.states:
                if not any(field.name == "current_state" for field in queryset.model._meta.get_fields()):
                    continue
                rule &= Q(current_state__in=permission.states)
            row_rule = cls._row_condition_query(queryset.model, permission.row_condition, user)
            if row_rule is not None:
                allowed |= rule & row_rule
        return queryset.filter(allowed).distinct()

    @classmethod
    def _permissions(cls, user, action, activity):
        if user.is_superuser:
            return CRUDPermission.objects.filter(activity=activity)
        assigned_nodes = OrganisationChart.objects.filter(group__in=user.groups.all())
        inherited_ids = {ancestor.pk for node in assigned_nodes for ancestor in node.get_ancestors(include_self=True)}
        if not inherited_ids:
            return CRUDPermission.objects.none()
        return CRUDPermission.objects.filter(
            organisation_id__in=inherited_ids,
            activity=activity,
            **{cls.ACTION_FIELDS[action]: True},
        )

    @staticmethod
    def _row_condition_query(model, condition, user):
        if not condition:
            return Q()
        field = condition.get("field")
        operator = condition.get("op")
        expected = condition.get("value")
        if not field or operator not in {"eq", "ne"}:
            return None
        field_model = model
        parts = field.split("__")
        for index, part in enumerate(parts):
            try:
                model_field = field_model._meta.get_field(part)
            except FieldDoesNotExist:
                return None
            if index < len(parts) - 1:
                if not model_field.is_relation or model_field.related_model is None:
                    return None
                field_model = model_field.related_model
        if expected == "$current_user":
            expected = user
        lookup = f"{field}__exact"
        query = Q(**{lookup: expected})
        return query if operator == "eq" else ~query


def visible_activity(user):
    return Activity.objects.filter(is_menu=True).order_by("sort_order", "name") if user.is_superuser else [
        activity for activity in Activity.objects.filter(is_menu=True).order_by("sort_order", "name")
        if PermissionService.can(user, "read", activity=activity)
    ]