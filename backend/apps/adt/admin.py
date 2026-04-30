from django.contrib import admin
from .models import Ward, Room, Bed, Admission, TransferLog, DischargeSummary


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward_type', 'capacity', 'branch', 'is_active')
    list_filter = ('ward_type', 'is_active', 'branch')
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('ward', 'room_number', 'room_type', 'capacity')
    list_filter = ('room_type', 'ward')
    search_fields = ('room_number',)


@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('room', 'bed_number', 'bed_type', 'status')
    list_filter = ('status', 'bed_type')
    search_fields = ('bed_number',)


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'ward', 'admission_date', 'admission_type', 'is_discharged')
    list_filter = ('admission_type', 'is_discharged', 'ward')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__patient_no')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TransferLog)
class TransferLogAdmin(admin.ModelAdmin):
    list_display = ('admission', 'from_ward', 'to_ward', 'transfer_date')
    list_filter = ('from_ward', 'to_ward')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DischargeSummary)
class DischargeSummaryAdmin(admin.ModelAdmin):
    list_display = ('admission', 'discharge_date')
    readonly_fields = ('created_at', 'updated_at')
