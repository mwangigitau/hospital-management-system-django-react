from django.db import models

from utils.models import BranchScopedModel


class HelpdeskTicket(BranchScopedModel):
    STATUS_CHOICES = [('open', 'Open'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('closed', 'Closed')]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, default='normal')
    assigned_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='helpdesk_tickets')

    def __str__(self):
        return self.title
