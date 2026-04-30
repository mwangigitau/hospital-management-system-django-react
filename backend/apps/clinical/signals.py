from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.broadcast import broadcast_event


@receiver(post_save, sender='clinical.Consultation')
def consultation_saved(sender, instance, created, **kwargs):
    if getattr(instance, '_skip_signal', False):
        return
    patient_name = str(instance.patient)
    broadcast_event(
        app='clinical',
        model='Consultation',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'doctor': str(instance.doctor),
            'date': str(instance.consultation_date.date()),
        },
        notification={
            'title': 'New Consultation' if created else 'Consultation Updated',
            'message': f'{patient_name} — Dr. {instance.doctor}',
            'level': 'info',
        },
    )


@receiver(post_save, sender='clinical.Prescription')
def prescription_saved(sender, instance, created, **kwargs):
    if getattr(instance, '_skip_signal', False):
        return
    patient_name = str(instance.consultation.patient)
    broadcast_event(
        app='clinical',
        model='Prescription',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'status': instance.status,
        },
        notification={
            'title': 'Prescription Issued' if created else 'Prescription Updated',
            'message': f'{patient_name} — {instance.get_status_display()}',
            'level': 'info',
        },
    )
