from django.apps import AppConfig


class CampeonatosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "campeonatos"

    def ready(self):
        import campeonatos.signals