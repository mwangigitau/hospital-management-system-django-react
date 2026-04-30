from django.db import models

from utils.models import BranchScopedModel


class InsuranceClaim(BranchScopedModel):
    STATUS_CHOICES = [('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='insurance_claims')
    invoice = models.ForeignKey('billing.Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='insurance_claims')
    claim_number = models.CharField(max_length=64, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.claim_number
