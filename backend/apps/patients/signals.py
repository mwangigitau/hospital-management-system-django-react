from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from utils.broadcast import broadcast_event


def _patient_summary(instance) -> dict:
    return {
        'patient_no': instance.patient_no,
        'full_name': instance.full_name,
        'phone': instance.phone,
        'gender': instance.gender,
    }


@receiver(post_save, sender='patients.Patient')
def patient_saved(sender, instance, created, **kwargs):
    if getattr(instance, '_skip_signal', False):
        return
    action = 'created' if created else 'updated'
    level = 'success' if created else 'info'
    verb = 'Registered' if created else 'Updated'
    broadcast_event(
        app='patients',
        model='Patient',
        action=action,
        object_id=str(instance.id),
        summary=_patient_summary(instance),
        notification={
            'title': f'Patient {verb}',
            'message': f'{instance.full_name} ({instance.patient_no})',
            'level': level,
        },
    )


@receiver(post_delete, sender='patients.Patient')
def patient_deleted(sender, instance, **kwargs):
    broadcast_event(
        app='patients',
        model='Patient',
        action='deleted',
        object_id=str(instance.id),
        summary=_patient_summary(instance),
        notification={
            'title': 'Patient Removed',
            'message': f'{instance.full_name} ({instance.patient_no})',
            'level': 'warning',
        },
    )
