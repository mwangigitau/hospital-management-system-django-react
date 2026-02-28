from django.contrib import admin

from .models import ImagingRequest, RadiologyReport

admin.site.register(ImagingRequest)
admin.site.register(RadiologyReport)
