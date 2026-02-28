from django.apps import AppConfig


class NursingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.nursing'
    verbose_name = 'Nursing'

    def ready(self):
        import apps.nursing.signals  # noqa: F401
