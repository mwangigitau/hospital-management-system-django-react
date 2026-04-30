from django.db import models
from utils.models import SoftDeleteModel, TimeStampedModel


class Consultation(SoftDeleteModel):
    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='consultations')
    doctor = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='consultations')
    admission = models.ForeignKey(
        'adt.Admission', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultations'
    )
    consultation_date = models.DateTimeField()
    chief_complaint = models.TextField()
    history = models.TextField(blank=True)
    examination = models.TextField(blank=True)
    diagnosis = models.JSONField(default=list)
    treatment_plan = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-consultation_date']

    def __str__(self):
        return f'{self.patient} - Dr. {self.doctor} on {self.consultation_date.date()}'


class Diagnosis(TimeStampedModel):
    DIAGNOSIS_TYPES = [
        ('primary', 'Primary'), ('secondary', 'Secondary'), ('differential', 'Differential'),
    ]

    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='diagnoses')
    icd10_code = models.CharField(max_length=20)
    icd10_description = models.CharField(max_length=255)
    diagnosis_type = models.CharField(max_length=20, choices=DIAGNOSIS_TYPES, default='primary')

    class Meta:
        verbose_name_plural = 'Diagnoses'

    def __str__(self):
        return f'{self.icd10_code} - {self.icd10_description}'


class Prescription(SoftDeleteModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'), ('active', 'Active'), ('dispensed', 'Dispensed'),
        ('completed', 'Completed'), ('cancelled', 'Cancelled'),
    ]

    consultation = models.ForeignKey(Consultation, on_delete=models.PROTECT, related_name='prescriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Prescription #{self.id} - {self.consultation.patient}'
