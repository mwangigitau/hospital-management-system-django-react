from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Ward, Room, Bed, Admission, TransferLog, DischargeSummary
from .serializers import (
    WardSerializer, RoomSerializer, BedSerializer,
    AdmissionSerializer, TransferLogSerializer, DischargeSummarySerializer,
)


class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['ward_type', 'branch', 'is_active']
    search_fields = ['name']
    ordering_fields = ['name']


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('ward').all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['ward', 'room_type']
    search_fields = ['room_number']


class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.select_related('room__ward').all()
    serializer_class = BedSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['room', 'bed_type', 'status']
    search_fields = ['bed_number']
    ordering_fields = ['bed_number', 'status']


class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.select_related('patient', 'bed', 'ward', 'attending_doctor').all()
    serializer_class = AdmissionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['patient', 'ward', 'admission_type', 'is_discharged']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__patient_no', 'diagnosis']
    ordering_fields = ['admission_date', 'discharge_date']
    ordering = ['-admission_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class TransferLogViewSet(viewsets.ModelViewSet):
    queryset = TransferLog.objects.select_related('admission', 'from_ward', 'to_ward').all()
    serializer_class = TransferLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['admission', 'from_ward', 'to_ward']
    ordering_fields = ['transfer_date']
    ordering = ['-transfer_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DischargeSummaryViewSet(viewsets.ModelViewSet):
    queryset = DischargeSummary.objects.select_related('admission').all()
    serializer_class = DischargeSummarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['admission']
    ordering_fields = ['discharge_date']
    ordering = ['-discharge_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
