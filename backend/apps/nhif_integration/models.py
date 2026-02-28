from django.db import models

from utils.models import BranchScopedModel


class NHIFApiLog(BranchScopedModel):
    endpoint = models.CharField(max_length=255)
    request_payload = models.JSONField(default=dict, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True)
    succeeded = models.BooleanField(default=False)
    attempt = models.PositiveSmallIntegerField(default=1)
    related_claim = models.ForeignKey('claims.InsuranceClaim', on_delete=models.SET_NULL, null=True, blank=True, related_name='nhif_logs')

    def __str__(self):
        return f'{self.endpoint} ({self.status_code})'
