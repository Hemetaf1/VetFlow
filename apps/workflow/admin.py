from django.contrib import admin
from .models import StateInTable, StateNavigation

admin.site.register((StateInTable, StateNavigation))