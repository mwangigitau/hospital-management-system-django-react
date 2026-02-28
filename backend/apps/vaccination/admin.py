from django.contrib import admin

from .models import ImmunizationRecord, VaccineBatch

admin.site.register(VaccineBatch)
admin.site.register(ImmunizationRecord)
