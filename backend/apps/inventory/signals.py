from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.broadcast import broadcast_event


@receiver(post_save, sender='inventory.StoreItem')
def store_item_saved(sender, instance, created, **kwargs):
    # Only broadcast if quantity changed (or newly created)
    broadcast_event(
        app='inventory',
        model='StoreItem',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'item': str(instance.item),
            'store': str(instance.store),
            'quantity': str(instance.quantity),
        },
        notification={
            'title': 'Inventory Updated',
            'message': f'{instance.item} in {instance.store}: qty {instance.quantity}',
            'level': 'warning' if float(instance.quantity) <= float(instance.item.reorder_level) else 'info',
        },
    )


@receiver(post_save, sender='inventory.StockTransfer')
def stock_transfer_saved(sender, instance, created, **kwargs):
    broadcast_event(
        app='inventory',
        model='StockTransfer',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'from_store': str(instance.from_store),
            'to_store': str(instance.to_store),
            'status': instance.status,
        },
        notification={
            'title': 'Stock Transfer Updated',
            'message': f'{instance.from_store} → {instance.to_store} ({instance.get_status_display()})',
            'level': 'info',
        },
    )
