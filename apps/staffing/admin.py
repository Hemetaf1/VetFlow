from django.contrib import admin
from .models import Shift, Staff, StaffAvailability

admin.site.register((Staff, Shift, StaffAvailability))