from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from utils.broadcast import broadcast_event, broadcast_notification

from .models import Category, Item, Store, StoreItem, StockTransfer
from .serializers import (
    CategorySerializer, ItemSerializer, StoreSerializer,
    StoreItemSerializer, StockTransferSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.select_related('category').all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description', 'barcode']
    ordering_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['store_type', 'branch']
    search_fields = ['name']


class StoreItemViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.select_related('store', 'item').all()
    serializer_class = StoreItemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['store', 'item']
    search_fields = ['item__name']
    ordering_fields = ['quantity']


class StockTransferViewSet(viewsets.ModelViewSet):
    queryset = StockTransfer.objects.select_related('from_store', 'to_store').prefetch_related('transfer_items').all()
    serializer_class = StockTransferSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['from_store', 'to_store', 'status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def barcode_scan(request):
    """
    Look up an inventory item by barcode and decrement its quantity by
    ``quantity`` (default 1) from the specified ``store``.

    POST body:
        barcode  (str)  – required
        store    (uuid) – required, store UUID to check out from
        quantity (int)  – optional, defaults to 1
    """
    barcode = request.data.get('barcode', '').strip()
    store_id = request.data.get('store')
    quantity = int(request.data.get('quantity', 1))

    if not barcode:
        return Response({'detail': 'barcode is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if not store_id:
        return Response({'detail': 'store is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if quantity < 1:
        return Response({'detail': 'quantity must be at least 1.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        item = Item.objects.get(barcode=barcode, is_deleted=False)
    except Item.DoesNotExist:
        return Response({'detail': 'No item found with this barcode.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        store_item = StoreItem.objects.select_related('store', 'item').get(
            item=item, store_id=store_id,
        )
    except StoreItem.DoesNotExist:
        return Response(
            {'detail': f'Item "{item.name}" is not stocked in the selected store.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if store_item.quantity < quantity:
        return Response(
            {'detail': f'Insufficient stock. Available: {store_item.quantity}.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    with transaction.atomic():
        store_item.quantity -= quantity
        store_item.save(update_fields=['quantity', 'updated_at'])

    # Real-time notification is triggered automatically by the StoreItem
    # post_save signal defined in signals.py.  Send an additional personal
    # notification to the scanning user so they get instant feedback.
    broadcast_notification(
        user_id=str(request.user.id),
        title='Barcode Checkout',
        message=f'{quantity} × {item.name} checked out from {store_item.store.name}.',
        level='success',
    )

    return Response({
        'detail': 'Item checked out successfully.',
        'item': ItemSerializer(item).data,
        'store_item': StoreItemSerializer(store_item).data,
        'quantity_removed': quantity,
    })
