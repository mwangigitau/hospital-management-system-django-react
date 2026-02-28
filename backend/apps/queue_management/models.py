from django.db import models

from utils.models import BranchScopedModel


class QueueToken(BranchScopedModel):
    STATUS_CHOICES = [('waiting', 'Waiting'), ('serving', 'Serving'), ('done', 'Done'), ('cancelled', 'Cancelled')]

    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name='queue_tokens')
    token_number = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('branch', 'department', 'token_number')

    def __str__(self):
        return f'{self.department} - {self.token_number}'
