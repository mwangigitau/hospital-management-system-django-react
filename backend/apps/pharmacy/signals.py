from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.broadcast import broadcast_event


@receiver(post_save, sender='pharmacy.DrugBatch')
def drug_batch_saved(sender, instance, created, **kwargs):
    broadcast_event(
        app='pharmacy',
        model='DrugBatch',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'drug': str(instance.drug),
            'batch_number': instance.batch_number,
            'quantity': instance.quantity,
            'expiry_date': str(instance.expiry_date),
        },
        notification={
            'title': 'Drug Batch Added' if created else 'Drug Batch Updated',
            'message': f'{instance.drug} — Batch {instance.batch_number} (qty: {instance.quantity})',
            'level': 'success' if created else 'info',
        },
    )


@receiver(post_save, sender='pharmacy.StockMovement')
def stock_movement_saved(sender, instance, created, **kwargs):
    if not created:
        return
    # Warn on stock-out movements for low-stock awareness
    level = 'warning' if instance.movement_type == 'out' else 'info'
    broadcast_event(
        app='pharmacy',
        model='StockMovement',
        action='created',
        object_id=str(instance.id),
        summary={
            'drug': str(instance.drug),
            'movement_type': instance.movement_type,
            'quantity': instance.quantity,
        },
        notification={
            'title': 'Stock Movement',
            'message': f'{instance.get_movement_type_display()} {abs(instance.quantity)} × {instance.drug}',
            'level': level,
        },
    )


@receiver(post_save, sender='pharmacy.PrescriptionItem')
def prescription_item_saved(sender, instance, created, **kwargs):
    broadcast_event(
        app='pharmacy',
        model='PrescriptionItem',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'drug': str(instance.drug),
            'status': instance.status,
            'quantity': instance.quantity,
        },
        notification={
            'title': 'Prescription Item Updated',
            'message': f'{instance.drug} — {instance.get_status_display()}',
            'level': 'info',
        },
    )
