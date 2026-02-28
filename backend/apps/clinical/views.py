from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Consultation, Diagnosis, Prescription
from .serializers import (
    ConsultationSerializer, ConsultationListSerializer,
    DiagnosisSerializer, PrescriptionSerializer,
)


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.select_related('patient', 'doctor', 'admission').prefetch_related(
        'diagnoses', 'prescriptions'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['patient', 'doctor', 'admission']
    search_fields = ['patient__first_name', 'patient__last_name', 'chief_complaint']
    ordering_fields = ['consultation_date']
    ordering = ['-consultation_date']

    def get_serializer_class(self):
        if self.action == 'list':
            return ConsultationListSerializer
        return ConsultationSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DiagnosisViewSet(viewsets.ModelViewSet):
    queryset = Diagnosis.objects.select_related('consultation').all()
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['consultation', 'diagnosis_type']
    search_fields = ['icd10_code', 'icd10_description']


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('consultation').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['consultation', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
