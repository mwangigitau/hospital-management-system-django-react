from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def cleanup_old_audit_logs(days=90):
    """Delete audit logs older than `days` days."""
    from .models import AuditLog
    cutoff = timezone.now() - timedelta(days=days)
    deleted, _ = AuditLog.objects.filter(timestamp__lt=cutoff).delete()
    return f'Deleted {deleted} audit log entries older than {days} days.'
