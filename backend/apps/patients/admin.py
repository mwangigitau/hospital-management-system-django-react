from django.contrib import admin
from .models import Patient, MedicalHistory, Allergy, NextOfKin, PatientFlag


class MedicalHistoryInline(admin.TabularInline):
    model = MedicalHistory
    extra = 0


class AllergyInline(admin.TabularInline):
    model = Allergy
    extra = 0


class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 0


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_no', 'first_name', 'last_name', 'gender', 'phone', 'is_active', 'branch')
    list_filter = ('gender', 'blood_group', 'is_active', 'branch')
    search_fields = ('first_name', 'last_name', 'patient_no', 'phone', 'nhif_number')
    readonly_fields = ('patient_no', 'created_at', 'updated_at')
    inlines = [MedicalHistoryInline, AllergyInline, NextOfKinInline]


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('patient', 'condition', 'diagnosed_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'condition')


@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'allergen', 'severity')
    list_filter = ('severity',)


@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = ('patient', 'name', 'relationship', 'phone')


@admin.register(PatientFlag)
class PatientFlagAdmin(admin.ModelAdmin):
    list_display = ('patient', 'flag_type')
    list_filter = ('flag_type',)
