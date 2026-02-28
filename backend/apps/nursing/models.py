from django.db import models
from utils.models import TimeStampedModel


class VitalSigns(TimeStampedModel):
    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='vital_signs')
    admission = models.ForeignKey(
        'adt.Admission', on_delete=models.SET_NULL, null=True, blank=True, related_name='vital_signs'
    )
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='°C')
    blood_pressure_systolic = models.PositiveSmallIntegerField(null=True, blank=True, help_text='mmHg')
    blood_pressure_diastolic = models.PositiveSmallIntegerField(null=True, blank=True, help_text='mmHg')
    pulse_rate = models.PositiveSmallIntegerField(null=True, blank=True, help_text='bpm')
    respiratory_rate = models.PositiveSmallIntegerField(null=True, blank=True, help_text='breaths/min')
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='%')
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text='kg')
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='cm')
    recorded_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='vital_signs_recorded')
    recorded_at = models.DateTimeField()

    class Meta:
        ordering = ['-recorded_at']
        verbose_name_plural = 'Vital signs'

    def __str__(self):
        return f'Vitals for {self.patient} at {self.recorded_at}'


class NursingNote(TimeStampedModel):
    NOTE_TYPES = [
        ('general', 'General'), ('medication', 'Medication'), ('observation', 'Observation'),
        ('incident', 'Incident'), ('handover', 'Handover'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='nursing_notes')
    admission = models.ForeignKey(
        'adt.Admission', on_delete=models.SET_NULL, null=True, blank=True, related_name='nursing_notes'
    )
    note = models.TextField()
    note_type = models.CharField(max_length=20, choices=NOTE_TYPES, default='general')
    recorded_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='nursing_notes_recorded')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.note_type} note for {self.patient}'


class MedicationAdministration(TimeStampedModel):
    ROUTE_CHOICES = [
        ('oral', 'Oral'), ('iv', 'Intravenous'), ('im', 'Intramuscular'),
        ('sc', 'Subcutaneous'), ('topical', 'Topical'), ('inhaled', 'Inhaled'),
    ]

    prescription = models.ForeignKey(
        'clinical.Prescription', on_delete=models.PROTECT, related_name='administrations'
    )
    drug_name = models.CharField(max_length=200)
    dose = models.CharField(max_length=100)
    route = models.CharField(max_length=20, choices=ROUTE_CHOICES)
    administered_at = models.DateTimeField()
    administered_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='medications_administered')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-administered_at']

    def __str__(self):
        return f'{self.drug_name} administered to {self.prescription.consultation.patient}'
