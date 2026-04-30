from django.contrib import admin

from .models import JournalEntry, LedgerAccount

admin.site.register(LedgerAccount)
admin.site.register(JournalEntry)
