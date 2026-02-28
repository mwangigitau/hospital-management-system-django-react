from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.uuid import uuid7


class Permission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True)
    module = models.CharField(max_length=50, db_index=True)

    class Meta:
        ordering = ['module', 'name']

    def __str__(self):
        return f'{self.module}: {self.name}'


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True, db_index=True)
    branch = models.CharField(max_length=100, blank=True, db_index=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [models.Index(fields=['last_name', 'first_name'])]

    def __str__(self):
        return f'{self.get_full_name()} ({self.username})'

    @property
    def full_name(self):
        return self.get_full_name()


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid7, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, db_index=True)  # CREATE, UPDATE, DELETE, LOGIN, LOGOUT
    model_name = models.CharField(max_length=100, db_index=True)
    object_id = models.CharField(max_length=100, blank=True, db_index=True)
    changes = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['action', 'model_name'])]

    def __str__(self):
        return f'{self.user} - {self.action} - {self.model_name} [{self.timestamp}]'
