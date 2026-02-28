from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TestCatalogViewSet, LabRequestViewSet, LabRequestItemViewSet, SampleViewSet, TestResultViewSet

router = DefaultRouter()
router.register('test-catalog', TestCatalogViewSet, basename='testcatalog')
router.register('requests', LabRequestViewSet, basename='labrequest')
router.register('request-items', LabRequestItemViewSet, basename='labrequestitem')
router.register('samples', SampleViewSet, basename='sample')
router.register('results', TestResultViewSet, basename='testresult')

urlpatterns = [
    path('', include(router.urls)),
]
