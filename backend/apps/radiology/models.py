from django.db import models

from utils.models import BranchScopedModel


class ImagingRequest(BranchScopedModel):
    STATUS_CHOICES = [('queued', 'Queued'), ('scheduled', 'Scheduled'), ('completed', 'Completed')]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='imaging_requests')
    modality = models.CharField(max_length=50)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')

    def __str__(self):
        return f'{self.patient} - {self.modality}'


class RadiologyReport(BranchScopedModel):
    imaging_request = models.OneToOneField(ImagingRequest, on_delete=models.CASCADE, related_name='report')
    findings = models.TextField()
    impression = models.TextField(blank=True)
    reported_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'Report {self.imaging_request_id}'
