from django.db import models

from utils.models import TimeStampedModel


class Branch(TimeStampedModel):
    name = models.CharField(max_length=150, unique=True)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class HospitalSetting(TimeStampedModel):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField(blank=True)

    def __str__(self):
        return self.key


class ModuleToggle(TimeStampedModel):
    module = models.CharField(max_length=100, unique=True)
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.module
