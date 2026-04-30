from django.contrib import admin
from .models import ServiceCharge, Invoice, InvoiceItem, Payment, Receipt


@admin.register(ServiceCharge)
class ServiceChargeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'department', 'is_active')
    list_filter = ('category', 'is_active', 'department')
    search_fields = ('name',)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'invoice_date', 'due_date', 'status', 'subtotal', 'discount', 'total')
    list_filter = ('status',)
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__patient_no')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [InvoiceItemInline]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'description', 'quantity', 'unit_price', 'total')
    search_fields = ('description',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'payment_date', 'amount', 'payment_method', 'reference', 'received_by')
    list_filter = ('payment_method',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'payment', 'created_at')
    search_fields = ('receipt_number',)
    readonly_fields = ('receipt_number', 'created_at', 'updated_at')
