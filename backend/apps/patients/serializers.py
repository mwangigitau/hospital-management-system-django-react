from rest_framework import serializers
from .models import Patient, MedicalHistory, Allergy, NextOfKin, PatientFlag


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['id', 'patient', 'condition', 'diagnosed_date', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = ['id', 'patient', 'allergen', 'reaction', 'severity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class NextOfKinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NextOfKin
        fields = ['id', 'patient', 'name', 'relationship', 'phone', 'address', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientFlagSerializer(serializers.ModelSerializer):
    flag_type_display = serializers.CharField(source='get_flag_type_display', read_only=True)

    class Meta:
        model = PatientFlag
        fields = ['id', 'patient', 'flag_type', 'flag_type_display', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    medical_histories = MedicalHistorySerializer(many=True, read_only=True)
    allergies = AllergySerializer(many=True, read_only=True)
    next_of_kin = NextOfKinSerializer(many=True, read_only=True)
    flags = PatientFlagSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'patient_no', 'first_name', 'last_name', 'full_name',
            'date_of_birth', 'gender', 'blood_group', 'phone', 'email',
            'address', 'nhif_number', 'is_active', 'branch',
            'medical_histories', 'allergies', 'next_of_kin', 'flags',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'patient_no', 'created_at', 'updated_at']


class PatientListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = ['id', 'patient_no', 'first_name', 'last_name', 'full_name',
                  'date_of_birth', 'gender', 'phone', 'is_active', 'branch']
