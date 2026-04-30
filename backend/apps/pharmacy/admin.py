from django.contrib import admin
from .models import Drug, DrugBatch, StockMovement, PrescriptionItem


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'generic_name', 'category', 'unit', 'reorder_level', 'is_controlled')
    list_filter = ('category', 'is_controlled')
    search_fields = ('name', 'generic_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DrugBatch)
class DrugBatchAdmin(admin.ModelAdmin):
    list_display = ('drug', 'batch_number', 'expiry_date', 'quantity', 'selling_price', 'supplier')
    list_filter = ('expiry_date',)
    search_fields = ('drug__name', 'batch_number', 'supplier')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('drug', 'movement_type', 'quantity', 'reference', 'created_at')
    list_filter = ('movement_type',)
    search_fields = ('drug__name', 'reference')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('prescription', 'drug', 'dose', 'frequency', 'quantity', 'dispensed_quantity', 'status')
    list_filter = ('status', 'frequency')
    search_fields = ('drug__name',)
    readonly_fields = ('created_at', 'updated_at')
