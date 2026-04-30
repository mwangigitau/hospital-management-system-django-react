from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Patient, MedicalHistory, Allergy, NextOfKin, PatientFlag
from .serializers import (
    PatientSerializer, PatientListSerializer,
    MedicalHistorySerializer, AllergySerializer,
    NextOfKinSerializer, PatientFlagSerializer,
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.prefetch_related(
        'medical_histories', 'allergies', 'next_of_kin', 'flags'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['gender', 'blood_group', 'is_active', 'branch']
    search_fields = ['first_name', 'last_name', 'patient_no', 'phone', 'email', 'nhif_number']
    ordering_fields = ['last_name', 'first_name', 'date_of_birth', 'created_at']
    ordering = ['last_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.select_related('patient').all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['patient']
    search_fields = ['condition', 'notes']


class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.select_related('patient').all()
    serializer_class = AllergySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['patient', 'severity']
    search_fields = ['allergen', 'reaction']


class NextOfKinViewSet(viewsets.ModelViewSet):
    queryset = NextOfKin.objects.select_related('patient').all()
    serializer_class = NextOfKinSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['patient']
    search_fields = ['name', 'relationship', 'phone']


class PatientFlagViewSet(viewsets.ModelViewSet):
    queryset = PatientFlag.objects.select_related('patient').all()
    serializer_class = PatientFlagSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'flag_type']
