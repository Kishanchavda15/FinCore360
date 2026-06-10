from django.apps import AppConfig


class PoliciesAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "policies_app"

    def ready(self):
        import policies_app.signals