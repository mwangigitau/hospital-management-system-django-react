from django.contrib import admin
from .models import TestCatalog, LabRequest, LabRequestItem, Sample, TestResult


@admin.register(TestCatalog)
class TestCatalogAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'price', 'turnaround_time')
    list_filter = ('category',)
    search_fields = ('name', 'code')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LabRequest)
class LabRequestAdmin(admin.ModelAdmin):
    list_display = ('patient', 'requested_by', 'status', 'priority', 'created_at')
    list_filter = ('status', 'priority')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__patient_no')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(LabRequestItem)
class LabRequestItemAdmin(admin.ModelAdmin):
    list_display = ('lab_request', 'test', 'status')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    list_display = ('lab_request_item', 'sample_type', 'collected_by', 'collected_at', 'barcode')
    list_filter = ('sample_type',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('lab_request_item', 'value', 'unit', 'is_critical', 'entered_by')
    list_filter = ('is_critical',)
    readonly_fields = ('created_at', 'updated_at')
