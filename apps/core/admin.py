from django.contrib import admin
from .models import Activity, CRUDPermission, OrganisationChart

admin.site.register((Activity, CRUDPermission, OrganisationChart))