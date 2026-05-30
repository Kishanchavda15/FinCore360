from django.apps import AppConfig


class UserFlowConfig(AppConfig):
    name = "accounts_app"

    def ready(self):
        import accounts_app.signale