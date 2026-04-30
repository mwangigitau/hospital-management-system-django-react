from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultationViewSet, DiagnosisViewSet, PrescriptionViewSet

router = DefaultRouter()
router.register('consultations', ConsultationViewSet, basename='consultation')
router.register('diagnoses', DiagnosisViewSet, basename='diagnosis')
router.register('prescriptions', PrescriptionViewSet, basename='prescription')

urlpatterns = [
    path('', include(router.urls)),
]
