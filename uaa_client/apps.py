from django.apps import AppConfig


class UaaClientConfig(AppConfig):
    name = "uaa_client"
    verbose_name = "UAA Client"

    def ready(self):
        from . import configuration

        configuration.validate_configuration()
