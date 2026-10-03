from django.contrib.auth.models import Group
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class OrganisationChart(MPTTModel):
    name = models.CharField(max_length=120)
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name="organisation_node")
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


class Activity(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    url_name = models.CharField(max_length=100, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    is_menu = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class CRUDPermission(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name="permissions")
    organisation = models.ForeignKey(OrganisationChart, on_delete=models.CASCADE, related_name="permissions")
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    states = models.JSONField(default=list, blank=True)
    row_condition = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = [("activity", "organisation")]

    def __str__(self):
        return f"{self.organisation}: {self.activity}"