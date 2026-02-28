from django.contrib import admin
from .models import VitalSigns, NursingNote, MedicationAdministration


@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'temperature', 'pulse_rate', 'blood_pressure_systolic', 'recorded_by', 'recorded_at')
    list_filter = ('recorded_at',)
    search_fields = ('patient__first_name', 'patient__last_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(NursingNote)
class NursingNoteAdmin(admin.ModelAdmin):
    list_display = ('patient', 'note_type', 'recorded_by', 'created_at')
    list_filter = ('note_type',)
    search_fields = ('patient__first_name', 'patient__last_name', 'note')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(MedicationAdministration)
class MedicationAdministrationAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'drug_name', 'dose', 'route', 'administered_by', 'administered_at')
    list_filter = ('route',)
    search_fields = ('drug_name',)
    readonly_fields = ('created_at', 'updated_at')
