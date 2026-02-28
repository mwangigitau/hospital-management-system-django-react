from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VitalSignsViewSet, NursingNoteViewSet, MedicationAdministrationViewSet

router = DefaultRouter()
router.register('vitals', VitalSignsViewSet, basename='vitalsigns')
router.register('notes', NursingNoteViewSet, basename='nursingnote')
router.register('medication-administrations', MedicationAdministrationViewSet, basename='medicationadministration')

urlpatterns = [
    path('', include(router.urls)),
]
