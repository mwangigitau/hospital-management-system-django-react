from django.db import models

from utils.models import BranchScopedModel


class Ambulance(BranchScopedModel):
    STATUS_CHOICES = [('available', 'Available'), ('on_trip', 'On Trip'), ('maintenance', 'Maintenance')]

    plate_number = models.CharField(max_length=30, unique=True)
    model_name = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.plate_number


class AmbulanceTrip(BranchScopedModel):
    TRIP_STATUS_CHOICES = [('dispatched', 'Dispatched'), ('in_transit', 'In Transit'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]

    ambulance = models.ForeignKey(Ambulance, on_delete=models.PROTECT, related_name='trips')
    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name='ambulance_trips')
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255, blank=True)
    trip_status = models.CharField(max_length=20, choices=TRIP_STATUS_CHOICES, default='dispatched')
    dispatched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ambulance} - {self.trip_status}'
