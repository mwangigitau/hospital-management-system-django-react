from rest_framework import serializers
from .models import Appointment, QueueTicket


class QueueTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueueTicket
        fields = ['id', 'appointment', 'token_number', 'status', 'called_at', 'served_at', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    doctor_name = serializers.StringRelatedField(source='doctor', read_only=True)
    queue_ticket = QueueTicketSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'department', 'appointment_date', 'appointment_time',
            'status', 'type', 'notes', 'queue_ticket',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AppointmentListSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    doctor_name = serializers.StringRelatedField(source='doctor', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name',
                  'department', 'appointment_date', 'appointment_time', 'status', 'type']
