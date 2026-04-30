from django.db import models

from utils.models import BranchScopedModel


class Referral(BranchScopedModel):
    STATUS_CHOICES = [('new', 'New'), ('approved', 'Approved'), ('paid', 'Paid')]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='referrals')
    referring_doctor = models.CharField(max_length=200)
    commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f'{self.referring_doctor} - {self.patient}'
