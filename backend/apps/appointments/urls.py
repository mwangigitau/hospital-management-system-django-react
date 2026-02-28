from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, QueueTicketViewSet

router = DefaultRouter()
router.register('', AppointmentViewSet, basename='appointment')
router.register('queue-tickets', QueueTicketViewSet, basename='queueticket')

urlpatterns = [
    path('', include(router.urls)),
]
