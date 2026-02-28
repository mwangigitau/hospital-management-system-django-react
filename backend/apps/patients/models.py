import uuid
from django.db import models
from utils.models import SoftDeleteModel, SoftDeleteManager, TimeStampedModel


def generate_patient_no():
    import random
    return f'P{random.randint(100000, 999999)}'


class Patient(SoftDeleteModel):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ]

    patient_no = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    nhif_number = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    branch = models.CharField(max_length=100, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.patient_no})'

    def save(self, *args, **kwargs):
        if not self.patient_no:
            patient_no = generate_patient_no()
            while Patient.all_objects.filter(patient_no=patient_no).exists():
                patient_no = generate_patient_no()
            self.patient_no = patient_no
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class MedicalHistory(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    condition = models.CharField(max_length=200)
    diagnosed_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Medical histories'
        ordering = ['-diagnosed_date']

    def __str__(self):
        return f'{self.patient} - {self.condition}'


class Allergy(TimeStampedModel):
    SEVERITY_CHOICES = [('mild', 'Mild'), ('moderate', 'Moderate'), ('severe', 'Severe')]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    allergen = models.CharField(max_length=200)
    reaction = models.CharField(max_length=200, blank=True)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='mild')

    class Meta:
        verbose_name_plural = 'Allergies'

    def __str__(self):
        return f'{self.patient} - {self.allergen} ({self.severity})'


class NextOfKin(TimeStampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='next_of_kin')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} ({self.relationship}) - {self.patient}'


class PatientFlag(TimeStampedModel):
    FLAG_TYPES = [
        ('allergy', 'Allergy Alert'),
        ('vip', 'VIP Patient'),
        ('risk', 'High Risk'),
        ('infection', 'Infection Control'),
        ('other', 'Other'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='flags')
    flag_type = models.CharField(max_length=20, choices=FLAG_TYPES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.patient} - {self.get_flag_type_display()}'
