from django.apps import AppConfig


class SignalsExampleConfig(AppConfig):
    name = 'signals_example'

    def ready(self):
        import signals_example.signals
