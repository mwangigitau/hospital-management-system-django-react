from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, MedicalHistoryViewSet, AllergyViewSet, NextOfKinViewSet, PatientFlagViewSet

router = DefaultRouter()
router.register('', PatientViewSet, basename='patient')
router.register('medical-histories', MedicalHistoryViewSet, basename='medicalhistory')
router.register('allergies', AllergyViewSet, basename='allergy')
router.register('next-of-kin', NextOfKinViewSet, basename='nextofkin')
router.register('flags', PatientFlagViewSet, basename='patientflag')

urlpatterns = [
    path('', include(router.urls)),
]
