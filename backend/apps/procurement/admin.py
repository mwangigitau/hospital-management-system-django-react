from django.contrib import admin

from .models import GoodsReceivedNote, PurchaseOrder, PurchaseRequisition, Supplier

admin.site.register(Supplier)
admin.site.register(PurchaseRequisition)
admin.site.register(PurchaseOrder)
admin.site.register(GoodsReceivedNote)
