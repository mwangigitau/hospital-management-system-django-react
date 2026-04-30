from django.apps import AppConfig


class AdtConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.adt'
    verbose_name = 'ADT (Admission, Discharge, Transfer)'

    def ready(self):
        import apps.adt.signals  # noqa: F401
