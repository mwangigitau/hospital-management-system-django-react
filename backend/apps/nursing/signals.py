from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.broadcast import broadcast_event


@receiver(post_save, sender='nursing.VitalSigns')
def vitals_saved(sender, instance, created, **kwargs):
    if not created:
        return
    patient_name = str(instance.patient)
    broadcast_event(
        app='nursing',
        model='VitalSigns',
        action='created',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'recorded_at': str(instance.recorded_at),
            'temperature': str(instance.temperature) if instance.temperature else None,
            'pulse_rate': instance.pulse_rate,
            'oxygen_saturation': str(instance.oxygen_saturation) if instance.oxygen_saturation else None,
        },
        notification={
            'title': 'Vitals Recorded',
            'message': f'New vitals recorded for {patient_name}',
            'level': 'info',
        },
    )


@receiver(post_save, sender='nursing.NursingNote')
def nursing_note_saved(sender, instance, created, **kwargs):
    if not created:
        return
    patient_name = str(instance.patient)
    broadcast_event(
        app='nursing',
        model='NursingNote',
        action='created',
        object_id=str(instance.id),
        summary={
            'patient': patient_name,
            'note_type': instance.note_type,
        },
        notification={
            'title': 'Nursing Note Added',
            'message': f'{instance.get_note_type_display()} note for {patient_name}',
            'level': 'info',
        },
    )
