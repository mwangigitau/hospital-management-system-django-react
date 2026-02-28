from rest_framework import serializers
from .models import Consultation, Diagnosis, Prescription


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ['id', 'consultation', 'icd10_code', 'icd10_description', 'diagnosis_type', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['id', 'consultation', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConsultationSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    doctor_name = serializers.StringRelatedField(source='doctor', read_only=True)
    diagnoses = DiagnosisSerializer(many=True, read_only=True)
    prescriptions = PrescriptionSerializer(many=True, read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name', 'admission',
            'consultation_date', 'chief_complaint', 'history', 'examination',
            'diagnosis', 'treatment_plan', 'notes',
            'diagnoses', 'prescriptions',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ConsultationListSerializer(serializers.ModelSerializer):
    patient_name = serializers.StringRelatedField(source='patient', read_only=True)
    doctor_name = serializers.StringRelatedField(source='doctor', read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'patient', 'patient_name', 'doctor', 'doctor_name',
                  'consultation_date', 'chief_complaint']
