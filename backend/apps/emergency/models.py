from django.db import models

from utils.models import BranchScopedModel


class EmergencyVisit(BranchScopedModel):
    TRIAGE_CHOICES = [('critical', 'Critical'), ('urgent', 'Urgent'), ('stable', 'Stable')]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='emergency_visits')
    triage_level = models.CharField(max_length=20, choices=TRIAGE_CHOICES)
    arrival_mode = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    admitted = models.BooleanField(default=False)

    def __str__(self):
        return f'Emergency {self.patient}'
