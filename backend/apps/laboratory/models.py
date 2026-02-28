from django.db import models
from utils.models import TimeStampedModel, SoftDeleteModel


class TestCatalog(SoftDeleteModel):
    CATEGORIES = [
        ('hematology', 'Hematology'), ('biochemistry', 'Biochemistry'),
        ('microbiology', 'Microbiology'), ('immunology', 'Immunology'),
        ('urinalysis', 'Urinalysis'), ('radiology', 'Radiology'), ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    normal_range = models.CharField(max_length=200, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    turnaround_time = models.PositiveIntegerField(help_text='Hours', default=24)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.code} - {self.name}'


class LabRequest(SoftDeleteModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('sample_collected', 'Sample Collected'),
        ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'),
    ]
    PRIORITY_CHOICES = [('routine', 'Routine'), ('urgent', 'Urgent'), ('stat', 'STAT')]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='lab_requests')
    requested_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='lab_requests_made')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='routine')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Lab Request for {self.patient} ({self.priority})'


class LabRequestItem(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('sample_collected', 'Sample Collected'),
        ('in_progress', 'In Progress'), ('resulted', 'Resulted'), ('verified', 'Verified'),
    ]

    lab_request = models.ForeignKey(LabRequest, on_delete=models.CASCADE, related_name='items')
    test = models.ForeignKey(TestCatalog, on_delete=models.PROTECT, related_name='request_items')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.test} for {self.lab_request.patient}'


class Sample(TimeStampedModel):
    SAMPLE_TYPES = [
        ('blood', 'Blood'), ('urine', 'Urine'), ('stool', 'Stool'),
        ('sputum', 'Sputum'), ('swab', 'Swab'), ('csf', 'CSF'), ('other', 'Other'),
    ]

    lab_request_item = models.ForeignKey(LabRequestItem, on_delete=models.CASCADE, related_name='samples')
    sample_type = models.CharField(max_length=20, choices=SAMPLE_TYPES)
    collected_at = models.DateTimeField()
    collected_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='samples_collected')
    barcode = models.CharField(max_length=100, blank=True, unique=True, null=True)

    def __str__(self):
        return f'{self.sample_type} sample - {self.lab_request_item}'


class TestResult(TimeStampedModel):
    lab_request_item = models.OneToOneField(LabRequestItem, on_delete=models.CASCADE, related_name='result')
    value = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, blank=True)
    normal_range = models.CharField(max_length=200, blank=True)
    is_critical = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    entered_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='test_results_entered')

    def __str__(self):
        return f'Result for {self.lab_request_item}: {self.value}'
