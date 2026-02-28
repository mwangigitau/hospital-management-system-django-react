from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DrugViewSet, DrugBatchViewSet, StockMovementViewSet, PrescriptionItemViewSet

router = DefaultRouter()
router.register('drugs', DrugViewSet, basename='drug')
router.register('drug-batches', DrugBatchViewSet, basename='drugbatch')
router.register('stock-movements', StockMovementViewSet, basename='stockmovement')
router.register('prescription-items', PrescriptionItemViewSet, basename='prescriptionitem')

urlpatterns = [
    path('', include(router.urls)),
]
