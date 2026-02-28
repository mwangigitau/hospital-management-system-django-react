from django.contrib import admin

from .models import Ambulance, AmbulanceTrip

admin.site.register(Ambulance)
admin.site.register(AmbulanceTrip)
