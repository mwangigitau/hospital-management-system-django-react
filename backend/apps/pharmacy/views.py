from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from utils.broadcast import broadcast_notification

from .models import Drug, DrugBatch, StockMovement, PrescriptionItem
from .serializers import DrugSerializer, DrugBatchSerializer, StockMovementSerializer, PrescriptionItemSerializer


class DrugViewSet(viewsets.ModelViewSet):
    queryset = Drug.objects.all()
    serializer_class = DrugSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'is_controlled']
    search_fields = ['name', 'generic_name', 'barcode']
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def barcode_scan(request):
    """
    Look up a drug by barcode and dispense it by creating a stock-out
    movement against the earliest-expiring batch with available quantity.

    POST body:
        barcode  (str) – required
        quantity (int) – optional, defaults to 1
        notes    (str) – optional
    """
    barcode = request.data.get('barcode', '').strip()
    quantity = int(request.data.get('quantity', 1))
    notes = request.data.get('notes', '')

    if not barcode:
        return Response({'detail': 'barcode is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if quantity < 1:
        return Response({'detail': 'quantity must be at least 1.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        drug = Drug.objects.get(barcode=barcode, is_deleted=False)
    except Drug.DoesNotExist:
        return Response({'detail': 'No drug found with this barcode.'}, status=status.HTTP_404_NOT_FOUND)

    # Find the earliest-expiring batch with enough stock (FEFO)
    batch = (
        DrugBatch.objects
        .filter(drug=drug, quantity__gte=quantity)
        .order_by('expiry_date')
        .first()
    )
    if batch is None:
        return Response(
            {'detail': f'Insufficient stock for "{drug.name}".'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        batch.quantity -= quantity
        batch.save(update_fields=['quantity', 'updated_at'])

        movement = StockMovement.objects.create(
            drug=drug,
            batch=batch,
            movement_type='out',
            quantity=quantity,
            reference=f'barcode-scan:{barcode}',
            notes=notes or f'Dispensed via barcode scan by {request.user.username}',
        )

    # The StockMovement post_save signal broadcasts to all subscribers.
    # Send an additional personal notification to the scanning user.
    broadcast_notification(
        user_id=str(request.user.id),
        title='Drug Dispensed',
        message=f'{quantity} × {drug.name} dispensed (batch {batch.batch_number}).',
        level='success',
    )

    return Response({
        'detail': 'Drug dispensed successfully.',
        'drug': DrugSerializer(drug).data,
        'batch': DrugBatchSerializer(batch).data,
        'movement': StockMovementSerializer(movement).data,
        'quantity_dispensed': quantity,
    })
