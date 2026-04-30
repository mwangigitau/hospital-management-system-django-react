from django.contrib import admin
from .models import Appointment, QueueTicket


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'department', 'appointment_date', 'appointment_time', 'status', 'type')
    list_filter = ('status', 'type', 'department', 'appointment_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'patient__patient_no', 'doctor__last_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QueueTicket)
class QueueTicketAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'token_number', 'status', 'called_at', 'served_at')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')
