from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.broadcast import broadcast_event


@receiver(post_save, sender='adt.Bed')
def bed_saved(sender, instance, created, **kwargs):
    broadcast_event(
        app='adt',
        model='Bed',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'bed_number': instance.bed_number,
            'status': instance.status,
            'room': str(instance.room),
        },
        notification={
            'title': 'Bed Status Changed' if not created else 'Bed Added',
            'message': f'Bed {instance.bed_number} is now {instance.get_status_display()}',
            'level': 'info',
        },
    )


@receiver(post_save, sender='adt.Admission')
def admission_saved(sender, instance, created, **kwargs):
    if getattr(instance, '_skip_signal', False):
        return
    action = 'created' if created else 'updated'
    patient_name = str(instance.patient)
    notification = {
        'title': 'New Admission' if created else 'Admission Updated',
        'message': f'{patient_name} admitted to {instance.ward}',
        'level': 'success' if created else 'info',
    }
    if not created and instance.is_discharged:
        notification = {
            'title': 'Patient Discharged',
            'message': f'{patient_name} has been discharged from {instance.ward}',
            'level': 'warning',
        }
    broadcast_event(
        app='adt',
        model='Admission',
        action=action,
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'ward': str(instance.ward),
            'is_discharged': instance.is_discharged,
        },
        notification=notification,
    )


@receiver(post_save, sender='adt.TransferLog')
def transfer_saved(sender, instance, created, **kwargs):
    if not created:
        return
    patient_name = str(instance.admission.patient)
    broadcast_event(
        app='adt',
        model='TransferLog',
        action='created',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'from_ward': str(instance.from_ward),
            'to_ward': str(instance.to_ward),
        },
        notification={
            'title': 'Patient Transferred',
            'message': f'{patient_name}: {instance.from_ward} → {instance.to_ward}',
            'level': 'info',
        },
    )


@receiver(post_save, sender='adt.DischargeSummary')
def discharge_summary_saved(sender, instance, created, **kwargs):
    if not created:
        return
    patient_name = str(instance.admission.patient)
    broadcast_event(
        app='adt',
        model='DischargeSummary',
        action='created',
        object_id=str(instance.id),
        summary={'patient': patient_name},
        notification={
            'title': 'Discharge Summary Created',
            'message': f'Discharge summary ready for {patient_name}',
            'level': 'info',
        },
    )
