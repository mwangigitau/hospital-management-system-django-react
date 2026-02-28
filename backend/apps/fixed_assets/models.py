from django.db import models

from utils.models import BranchScopedModel


class Asset(BranchScopedModel):
    asset_tag = models.CharField(max_length=60, unique=True)
    name = models.CharField(max_length=200)
    purchase_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    purchase_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.asset_tag


class AssetMaintenanceLog(BranchScopedModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_date = models.DateField()
    notes = models.TextField(blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.asset} @ {self.maintenance_date}'
