from django.apps import AppConfig


class AppAdminConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_admin'

    def ready(self):
        import app_admin.signals
