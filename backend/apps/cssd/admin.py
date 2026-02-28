from django.contrib import admin

from .models import Instrument, SterilizationCycle

admin.site.register(Instrument)
admin.site.register(SterilizationCycle)
