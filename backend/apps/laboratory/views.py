from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import TestCatalog, LabRequest, LabRequestItem, Sample, TestResult
from .serializers import (
    TestCatalogSerializer, LabRequestSerializer,
    LabRequestItemSerializer, SampleSerializer, TestResultSerializer,
)


class TestCatalogViewSet(viewsets.ModelViewSet):
    queryset = TestCatalog.objects.all()
    serializer_class = TestCatalogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'price']
    ordering = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class LabRequestViewSet(viewsets.ModelViewSet):
    queryset = LabRequest.objects.select_related('patient', 'requested_by').prefetch_related('items__result').all()
    serializer_class = LabRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['patient', 'status', 'priority']
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__patient_no']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(requested_by=self.request.user, created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class LabRequestItemViewSet(viewsets.ModelViewSet):
    queryset = LabRequestItem.objects.select_related('lab_request', 'test').all()
    serializer_class = LabRequestItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lab_request', 'test', 'status']


class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.select_related('lab_request_item', 'collected_by').all()
    serializer_class = SampleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['lab_request_item', 'sample_type']
    ordering_fields = ['collected_at']
    ordering = ['-collected_at']

    def perform_create(self, serializer):
        serializer.save(collected_by=self.request.user)


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.select_related('lab_request_item', 'entered_by').all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['lab_request_item', 'is_critical']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(entered_by=self.request.user)
