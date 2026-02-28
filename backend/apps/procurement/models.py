from django.db import models

from utils.models import BranchScopedModel


class Supplier(BranchScopedModel):
    name = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name


class PurchaseRequisition(BranchScopedModel):
    STATUS_CHOICES = [('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    requested_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'Requisition {self.id}'


class PurchaseOrder(BranchScopedModel):
    STATUS_CHOICES = [('draft', 'Draft'), ('issued', 'Issued'), ('partially_received', 'Partially Received'), ('received', 'Received')]

    requisition = models.ForeignKey(PurchaseRequisition, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchase_orders')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='purchase_orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    expected_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'PO {self.id}'


class GoodsReceivedNote(BranchScopedModel):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='grns')
    received_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'GRN {self.id}'
