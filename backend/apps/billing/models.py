import uuid
from django.db import models
from utils.models import TimeStampedModel, SoftDeleteModel


class ServiceCharge(TimeStampedModel):
    CATEGORIES = [
        ('consultation', 'Consultation'), ('procedure', 'Procedure'),
        ('laboratory', 'Laboratory'), ('pharmacy', 'Pharmacy'), ('nursing', 'Nursing'),
        ('accommodation', 'Accommodation'), ('radiology', 'Radiology'), ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.price}'


class Invoice(SoftDeleteModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'), ('issued', 'Issued'), ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'), ('overdue', 'Overdue'), ('cancelled', 'Cancelled'), ('waived', 'Waived'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='invoices')
    admission = models.ForeignKey(
        'adt.Admission', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices'
    )
    invoice_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-invoice_date']

    def __str__(self):
        return f'Invoice #{self.id} - {self.patient} ({self.status})'


class InvoiceItem(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(ServiceCharge, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=300)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.description} x{self.quantity}'


class Payment(TimeStampedModel):
    PAYMENT_METHODS = [
        ('cash', 'Cash'), ('mpesa', 'M-Pesa'), ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'), ('insurance', 'Insurance'), ('nhif', 'NHIF'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='payments')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    reference = models.CharField(max_length=100, blank=True)
    received_by = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='payments_received')

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f'Payment of {self.amount} for {self.invoice}'


def generate_receipt_number():
    import random
    return f'RCP{random.randint(1000000, 9999999)}'


class Receipt(TimeStampedModel):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='receipt')
    receipt_number = models.CharField(max_length=20, unique=True, editable=False)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            num = generate_receipt_number()
            while Receipt.objects.filter(receipt_number=num).exists():
                num = generate_receipt_number()
            self.receipt_number = num
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Receipt {self.receipt_number}'
