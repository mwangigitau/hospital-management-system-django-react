from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import VitalSigns, NursingNote, MedicationAdministration
from .serializers import VitalSignsSerializer, NursingNoteSerializer, MedicationAdministrationSerializer


class VitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.select_related('patient', 'recorded_by').all()
    serializer_class = VitalSignsSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['patient', 'admission']
    ordering_fields = ['recorded_at']
    ordering = ['-recorded_at']

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)


class NursingNoteViewSet(viewsets.ModelViewSet):
    queryset = NursingNote.objects.select_related('patient', 'recorded_by').all()
    serializer_class = NursingNoteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['patient', 'admission', 'note_type']
    search_fields = ['note']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(recorded_by=self.request.user)


class MedicationAdministrationViewSet(viewsets.ModelViewSet):
    queryset = MedicationAdministration.objects.select_related('prescription', 'administered_by').all()
    serializer_class = MedicationAdministrationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['prescription']
    search_fields = ['drug_name']
    ordering_fields = ['administered_at']
    ordering = ['-administered_at']

    def perform_create(self, serializer):
        serializer.save(administered_by=self.request.user)
