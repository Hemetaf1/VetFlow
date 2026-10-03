from django.contrib import admin
from .models import Equipment, ResourceAllocate, Room

admin.site.register((Room, Equipment, ResourceAllocate))