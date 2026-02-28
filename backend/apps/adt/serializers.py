from rest_framework import serializers
from .models import Ward, Room, Bed, Admission, TransferLog, DischargeSummary


class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['id', 'name', 'ward_type', 'capacity', 'branch', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoomSerializer(serializers.ModelSerializer):
    ward_name = serializers.StringRelatedField(source='ward', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'ward', 'ward_name', 'room_number', 'room_type', 'capacity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BedSerializer(serializers.ModelSerializer):
    room_display = serializers.StringRelatedField(source='room', read_only=True)

    class Meta:
        model = Bed
        fields = ['id', 'room', 'room_display', 'bed_number', 'bed_type', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdmissionSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    ward_name = serializers.StringRelatedField(source='ward', read_only=True)
    doctor_name = serializers.StringRelatedField(source='attending_doctor', read_only=True)

    class Meta:
        model = Admission
        fields = [
            'id', 'patient', 'patient_name', 'bed', 'ward', 'ward_name',
            'admission_date', 'discharge_date', 'admission_type', 'diagnosis',
            'attending_doctor', 'doctor_name', 'is_discharged',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class TransferLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferLog
        fields = [
            'id', 'admission', 'from_ward', 'to_ward', 'from_bed', 'to_bed',
            'transfer_date', 'reason', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DischargeSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DischargeSummary
        fields = [
            'id', 'admission', 'discharge_date', 'diagnosis',
            'treatment_summary', 'follow_up_instructions', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
