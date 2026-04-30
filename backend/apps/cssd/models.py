from django.db import models

from utils.models import BranchScopedModel


class Instrument(BranchScopedModel):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SterilizationCycle(BranchScopedModel):
    STATUS_CHOICES = [('scheduled', 'Scheduled'), ('running', 'Running'), ('completed', 'Completed')]

    cycle_number = models.CharField(max_length=50, unique=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    def __str__(self):
        return self.cycle_number
