from django.db import models
from utils.models import TimeStampedModel, SoftDeleteModel
from utils.uuid import uuid7


class Category(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Item(SoftDeleteModel):
    name = models.CharField(max_length=200)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    unit = models.CharField(max_length=50)
    reorder_level = models.PositiveIntegerField(default=5)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.unit})'


class Store(TimeStampedModel):
    STORE_TYPES = [
        ('main', 'Main Store'), ('pharmacy', 'Pharmacy'), ('ward', 'Ward Store'),
        ('lab', 'Laboratory'), ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    store_type = models.CharField(max_length=20, choices=STORE_TYPES, default='other')
    location = models.CharField(max_length=200, blank=True)
    branch = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.get_store_type_display()})'


class StoreItem(TimeStampedModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='store_items')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('store', 'item')

    def __str__(self):
        return f'{self.item} in {self.store}: {self.quantity}'


class StockTransferItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    transfer = models.ForeignKey('StockTransfer', on_delete=models.CASCADE, related_name='transfer_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.item} x {self.quantity}'


class StockTransfer(TimeStampedModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'), ('pending', 'Pending'), ('approved', 'Approved'),
        ('in_transit', 'In Transit'), ('received', 'Received'), ('cancelled', 'Cancelled'),
    ]

    from_store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='transfers_out')
    to_store = models.ForeignKey(Store, on_delete=models.PROTECT, related_name='transfers_in')
    items = models.ManyToManyField(Item, through=StockTransferItem, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Transfer from {self.from_store} to {self.to_store} ({self.status})'
