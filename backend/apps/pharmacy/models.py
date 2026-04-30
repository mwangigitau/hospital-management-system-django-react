from django.db import models
from utils.models import TimeStampedModel, SoftDeleteModel


class Drug(SoftDeleteModel):
    CATEGORIES = [
        ('analgesic', 'Analgesic'), ('antibiotic', 'Antibiotic'), ('antiviral', 'Antiviral'),
        ('antifungal', 'Antifungal'), ('cardiovascular', 'Cardiovascular'),
        ('respiratory', 'Respiratory'), ('gastrointestinal', 'Gastrointestinal'),
        ('endocrine', 'Endocrine'), ('neurological', 'Neurological'), ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True, db_index=True)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORIES, default='other')
    unit = models.CharField(max_length=50, help_text='e.g. tablets, ml, capsules')
    reorder_level = models.PositiveIntegerField(default=10)
    description = models.TextField(blank=True)
    is_controlled = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.generic_name})'


class DrugBatch(TimeStampedModel):
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT, related_name='batches')
    batch_number = models.CharField(max_length=100)
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name_plural = 'Drug batches'
        ordering = ['expiry_date']

    def __str__(self):
        return f'{self.drug} - Batch {self.batch_number} (exp: {self.expiry_date})'


class StockMovement(TimeStampedModel):
    MOVEMENT_TYPES = [
        ('in', 'Stock In'), ('out', 'Stock Out'), ('adjustment', 'Adjustment'),
        ('return', 'Return'), ('expired', 'Expired'),
    ]

    drug = models.ForeignKey(Drug, on_delete=models.PROTECT, related_name='stock_movements')
    batch = models.ForeignKey(DrugBatch, on_delete=models.PROTECT, related_name='movements', null=True, blank=True)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.movement_type} {self.quantity} of {self.drug}'


class PrescriptionItem(TimeStampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'), ('dispensed', 'Dispensed'), ('partially_dispensed', 'Partially Dispensed'),
        ('cancelled', 'Cancelled'),
    ]
    FREQUENCY_CHOICES = [
        ('od', 'Once Daily'), ('bd', 'Twice Daily'), ('tds', 'Three Times Daily'),
        ('qds', 'Four Times Daily'), ('prn', 'As Needed'), ('stat', 'Immediately'),
    ]

    prescription = models.ForeignKey('clinical.Prescription', on_delete=models.PROTECT, related_name='items')
    drug = models.ForeignKey(Drug, on_delete=models.PROTECT, related_name='prescription_items')
    dose = models.CharField(max_length=100)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    duration = models.CharField(max_length=50, help_text='e.g. 7 days')
    quantity = models.PositiveIntegerField()
    dispensed_quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.drug} - {self.dose} {self.frequency}'
