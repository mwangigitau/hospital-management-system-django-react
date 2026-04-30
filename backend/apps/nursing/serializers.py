from rest_framework import serializers
from .models import VitalSigns, NursingNote, MedicationAdministration


class VitalSignsSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    recorded_by_name = serializers.StringRelatedField(source='recorded_by', read_only=True)

    class Meta:
        model = VitalSigns
        fields = [
            'id', 'patient', 'patient_name', 'admission',
            'temperature', 'blood_pressure_systolic', 'blood_pressure_diastolic',
            'pulse_rate', 'respiratory_rate', 'oxygen_saturation',
            'weight', 'height', 'recorded_by', 'recorded_by_name', 'recorded_at',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NursingNoteSerializer(serializers.ModelSerializer):
    recorded_by_name = serializers.StringRelatedField(source='recorded_by', read_only=True)

    class Meta:
        model = NursingNote
        fields = ['id', 'patient', 'admission', 'note', 'note_type',
                  'recorded_by', 'recorded_by_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MedicationAdministrationSerializer(serializers.ModelSerializer):
    administered_by_name = serializers.StringRelatedField(source='administered_by', read_only=True)

    class Meta:
        model = MedicationAdministration
        fields = [
            'id', 'prescription', 'drug_name', 'dose', 'route',
            'administered_at', 'administered_by', 'administered_by_name', 'notes',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
