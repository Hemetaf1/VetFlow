from django.contrib import admin
from .models import Owner, Patient, Procedure, ProcedureSession, Visit

admin.site.register((Owner, Patient, Procedure, ProcedureSession, Visit))