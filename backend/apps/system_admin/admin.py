from django.contrib import admin

from .models import Branch, HospitalSetting, ModuleToggle

admin.site.register(Branch)
admin.site.register(HospitalSetting)
admin.site.register(ModuleToggle)
