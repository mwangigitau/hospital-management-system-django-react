from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.broadcast import broadcast_event


@receiver(post_save, sender='laboratory.LabRequest')
def lab_request_saved(sender, instance, created, **kwargs):
    if getattr(instance, '_skip_signal', False):
        return
    patient_name = str(instance.patient)
    broadcast_event(
        app='laboratory',
        model='LabRequest',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'status': instance.status,
            'priority': instance.priority,
        },
        notification={
            'title': 'Lab Request Raised' if created else 'Lab Request Updated',
            'message': f'{patient_name} — {instance.get_priority_display()} ({instance.get_status_display()})',
            'level': 'warning' if instance.priority == 'stat' else 'info',
        },
    )


@receiver(post_save, sender='laboratory.TestResult')
def test_result_saved(sender, instance, created, **kwargs):
    if not created:
        return
    patient_name = str(instance.lab_request_item.lab_request.patient)
    test_name = str(instance.lab_request_item.test)
    level = 'error' if instance.is_critical else 'success'
    notification_title = '🚨 Critical Lab Result' if instance.is_critical else 'Lab Result Ready'
    broadcast_event(
        app='laboratory',
        model='TestResult',
        action='created',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'test': test_name,
            'value': instance.value,
            'is_critical': instance.is_critical,
        },
        notification={
            'title': notification_title,
            'message': f'{test_name}: {instance.value} — {patient_name}',
            'level': level,
        },
    )
