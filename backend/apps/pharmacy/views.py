from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Drug, DrugBatch, StockMovement, PrescriptionItem
from .serializers import DrugSerializer, DrugBatchSerializer, StockMovementSerializer, PrescriptionItemSerializer


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_controlled']
    search_fields = ['name', 'generic_name']
    ordering_fields = ['name', 'category']
    ordering = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DrugBatchViewSet(viewsets.ModelViewSet):
    queryset = DrugBatch.objects.select_related('drug').all()
    serializer_class = DrugBatchSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['drug', 'supplier']
    search_fields = ['batch_number', 'drug__name']
    ordering_fields = ['expiry_date', 'quantity']
    ordering = ['expiry_date']


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.select_related('drug', 'batch').all()
    serializer_class = StockMovementSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['drug', 'movement_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    queryset = PrescriptionItem.objects.select_related('prescription', 'drug').all()
    serializer_class = PrescriptionItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['prescription', 'drug', 'status']
    search_fields = ['drug__name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
