from django.apps import AppConfig


class ClientsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "clients_app"

    def ready(self):
        import clients_app.signals