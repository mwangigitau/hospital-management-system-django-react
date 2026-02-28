from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.broadcast import broadcast_event


@receiver(post_save, sender='appointments.Appointment')
def appointment_saved(sender, instance, created, **kwargs):
    if getattr(instance, '_skip_signal', False):
        return
    action = 'created' if created else 'updated'
    patient_name = str(instance.patient)
    broadcast_event(
        app='appointments',
        model='Appointment',
        action=action,
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'doctor': str(instance.doctor),
            'date': str(instance.appointment_date),
            'status': instance.status,
        },
        notification={
            'title': 'Appointment Booked' if created else 'Appointment Updated',
            'message': f'{patient_name} — {instance.appointment_date} ({instance.get_status_display()})',
            'level': 'success' if created else 'info',
        },
    )


@receiver(post_save, sender='appointments.QueueTicket')
def queue_ticket_saved(sender, instance, created, **kwargs):
    patient_name = str(instance.appointment.patient)
    broadcast_event(
        app='appointments',
        model='QueueTicket',
        action='created' if created else 'updated',
        object_id=str(instance.id),
        summary={
            'token': instance.token_number,
            'patient': patient_name,
            'status': instance.status,
        },
        notification={
            'title': 'Queue Updated',
            'message': f'Token {instance.token_number} — {patient_name} ({instance.get_status_display()})',
            'level': 'info',
        },
    )
