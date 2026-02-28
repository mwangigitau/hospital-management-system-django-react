from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WardViewSet, RoomViewSet, BedViewSet, AdmissionViewSet, TransferLogViewSet, DischargeSummaryViewSet

router = DefaultRouter()
router.register('wards', WardViewSet, basename='ward')
router.register('rooms', RoomViewSet, basename='room')
router.register('beds', BedViewSet, basename='bed')
router.register('admissions', AdmissionViewSet, basename='admission')
router.register('transfers', TransferLogViewSet, basename='transfer')
router.register('discharge-summaries', DischargeSummaryViewSet, basename='dischargesummary')

urlpatterns = [
    path('', include(router.urls)),
]
