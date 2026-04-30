from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Appointment, QueueTicket
from .serializers import AppointmentSerializer, AppointmentListSerializer, QueueTicketSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient', 'doctor').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'type', 'department', 'doctor', 'patient', 'appointment_date']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__patient_no', 'department']
    ordering_fields = ['appointment_date', 'appointment_time']
    ordering = ['-appointment_date', '-appointment_time']

    def get_serializer_class(self):
        if self.action == 'list':
            return AppointmentListSerializer
        return AppointmentSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class QueueTicketViewSet(viewsets.ModelViewSet):
    queryset = QueueTicket.objects.select_related('appointment__patient').all()
    serializer_class = QueueTicketSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'appointment']
    ordering_fields = ['token_number']
    ordering = ['token_number']
