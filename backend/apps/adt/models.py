from django.db import models
from utils.models import SoftDeleteModel, TimeStampedModel


class Ward(TimeStampedModel):
    WARD_TYPES = [
        ('general', 'General'), ('private', 'Private'), ('icu', 'ICU'),
        ('maternity', 'Maternity'), ('pediatric', 'Pediatric'), ('emergency', 'Emergency'),
    ]
    name = models.CharField(max_length=100)
    ward_type = models.CharField(max_length=20, choices=WARD_TYPES)
    capacity = models.PositiveIntegerField(default=0)
    branch = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Room(TimeStampedModel):
    ROOM_TYPES = [('general', 'General'), ('private', 'Private'), ('isolation', 'Isolation')]

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, default='general')
    capacity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('ward', 'room_number')
        ordering = ['room_number']

    def __str__(self):
        return f'{self.ward} - Room {self.room_number}'


class Bed(TimeStampedModel):
    BED_TYPES = [('standard', 'Standard'), ('icu', 'ICU'), ('maternity', 'Maternity')]
    BED_STATUS = [
        ('available', 'Available'), ('occupied', 'Occupied'),
        ('reserved', 'Reserved'), ('maintenance', 'Under Maintenance'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=20)
    bed_type = models.CharField(max_length=20, choices=BED_TYPES, default='standard')
    status = models.CharField(max_length=20, choices=BED_STATUS, default='available')

    class Meta:
        unique_together = ('room', 'bed_number')
        ordering = ['bed_number']

    def __str__(self):
        return f'{self.room} - Bed {self.bed_number} ({self.status})'


class Admission(SoftDeleteModel):
    ADMISSION_TYPES = [
        ('elective', 'Elective'), ('emergency', 'Emergency'), ('transfer', 'Transfer'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='admissions')
    bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name='admissions', null=True, blank=True)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name='admissions')
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(null=True, blank=True)
    admission_type = models.CharField(max_length=20, choices=ADMISSION_TYPES, default='elective')
    diagnosis = models.TextField(blank=True)
    attending_doctor = models.ForeignKey(
        'accounts.User', on_delete=models.PROTECT, related_name='admitted_patients'
    )
    is_discharged = models.BooleanField(default=False)

    class Meta:
        ordering = ['-admission_date']

    def __str__(self):
        return f'{self.patient} admitted {self.admission_date.date()}'


class TransferLog(TimeStampedModel):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='transfers')
    from_ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name='transfers_from')
    to_ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name='transfers_to')
    from_bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name='transfers_from', null=True, blank=True)
    to_bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name='transfers_to', null=True, blank=True)
    transfer_date = models.DateTimeField()
    reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-transfer_date']

    def __str__(self):
        return f'{self.admission.patient} transferred {self.transfer_date.date()}'


class DischargeSummary(TimeStampedModel):
    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='discharge_summary')
    discharge_date = models.DateTimeField()
    diagnosis = models.TextField()
    treatment_summary = models.TextField()
    follow_up_instructions = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Discharge summaries'

    def __str__(self):
        return f'Discharge: {self.admission.patient} on {self.discharge_date.date()}'
