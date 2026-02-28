from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.broadcast import broadcast_event


@receiver(post_save, sender='billing.Invoice')
def invoice_saved(sender, instance, created, **kwargs):
    if getattr(instance, '_skip_signal', False):
        return
    patient_name = str(instance.patient)
    broadcast_event(
        app='billing',
        model='Invoice',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'status': instance.status,
            'total': str(instance.total),
        },
        notification={
            'title': 'Invoice Created' if created else 'Invoice Updated',
            'message': f'{patient_name} — KES {instance.total} ({instance.get_status_display()})',
            'level': 'success' if created else 'info',
        },
    )


@receiver(post_save, sender='billing.Payment')
def payment_saved(sender, instance, created, **kwargs):
    if not created:
        return
    patient_name = str(instance.invoice.patient)
    broadcast_event(
        app='billing',
        model='Payment',
        action='created',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'amount': str(instance.amount),
            'method': instance.payment_method,
        },
        notification={
            'title': 'Payment Received',
            'message': f'KES {instance.amount} via {instance.get_payment_method_display()} — {patient_name}',
            'level': 'success',
        },
    )
