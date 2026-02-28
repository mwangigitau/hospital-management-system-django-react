from django.contrib import admin
from .models import Consultation, Diagnosis, Prescription


@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'consultation_date', 'chief_complaint')
    list_filter = ('consultation_date',)
    search_fields = ('patient__first_name', 'patient__last_name', 'chief_complaint')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'icd10_code', 'icd10_description', 'diagnosis_type')
    list_filter = ('diagnosis_type',)
    search_fields = ('icd10_code', 'icd10_description')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('consultation', 'status', 'created_at')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')
