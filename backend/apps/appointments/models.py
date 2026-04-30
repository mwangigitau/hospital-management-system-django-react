from django.db import models
from utils.models import SoftDeleteModel, TimeStampedModel


class Appointment(SoftDeleteModel):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'), ('confirmed', 'Confirmed'), ('arrived', 'Arrived'),
        ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    APPT_TYPES = [
        ('consultation', 'Consultation'), ('follow_up', 'Follow Up'),
        ('procedure', 'Procedure'), ('checkup', 'Checkup'),
    ]

    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='appointments')
    doctor = models.ForeignKey('accounts.User', on_delete=models.PROTECT, related_name='doctor_appointments')
    department = models.CharField(max_length=100)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    type = models.CharField(max_length=20, choices=APPT_TYPES, default='consultation')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def __str__(self):
        return f'{self.patient} - Dr. {self.doctor} on {self.appointment_date}'


class QueueTicket(TimeStampedModel):
    STATUS_CHOICES = [
        ('waiting', 'Waiting'), ('called', 'Called'), ('serving', 'Serving'), ('done', 'Done'), ('skipped', 'Skipped'),
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='queue_ticket')
    token_number = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    called_at = models.DateTimeField(null=True, blank=True)
    served_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['token_number']

    def __str__(self):
        return f'Token {self.token_number} - {self.appointment.patient}'
