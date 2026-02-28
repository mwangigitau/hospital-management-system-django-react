from django.db import models

from utils.models import BranchScopedModel


class VaccineBatch(BranchScopedModel):
    vaccine_name = models.CharField(max_length=150)
    batch_number = models.CharField(max_length=80, unique=True)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.vaccine_name} ({self.batch_number})'


class ImmunizationRecord(BranchScopedModel):
    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='immunizations')
    vaccine_batch = models.ForeignKey(VaccineBatch, on_delete=models.PROTECT, related_name='immunizations')
    administered_on = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.patient} - {self.vaccine_batch}'
