from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceChargeViewSet, InvoiceViewSet, InvoiceItemViewSet, PaymentViewSet, ReceiptViewSet

router = DefaultRouter()
router.register('service-charges', ServiceChargeViewSet, basename='servicecharge')
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('invoice-items', InvoiceItemViewSet, basename='invoiceitem')
router.register('payments', PaymentViewSet, basename='payment')
router.register('receipts', ReceiptViewSet, basename='receipt')

urlpatterns = [
    path('', include(router.urls)),
]
