from django.apps import AppConfig


class UserFlowConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"   # ADDED
    name = "accounts_app"

    def ready(self):
        import accounts_app.signale