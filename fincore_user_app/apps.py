from django.apps import AppConfig


class UserFlowConfig(AppConfig):
    name = "fincore_user_app"

    def ready(self):
        import fincore_user_app.signale