from django.contrib import admin
from .models import Category, Item, Store, StoreItem, StockTransfer, StockTransferItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'unit', 'reorder_level')
    list_filter = ('category',)
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'store_type', 'location', 'branch')
    list_filter = ('store_type', 'branch')
    search_fields = ('name',)


@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('store', 'item', 'quantity', 'unit_cost')
    list_filter = ('store',)
    search_fields = ('item__name',)


class StockTransferItemInline(admin.TabularInline):
    model = StockTransferItem
    extra = 0


@admin.register(StockTransfer)
class StockTransferAdmin(admin.ModelAdmin):
    list_display = ('from_store', 'to_store', 'status', 'created_at')
    list_filter = ('status',)
    inlines = [StockTransferItemInline]
    readonly_fields = ('created_at', 'updated_at')
