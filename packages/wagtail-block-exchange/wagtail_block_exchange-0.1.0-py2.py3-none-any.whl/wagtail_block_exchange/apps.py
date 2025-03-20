from django.apps import AppConfig


class WagtailBlockExchangeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wagtail_block_exchange'
    label = 'wagtail_block_exchange'
    verbose_name = 'Wagtail Block Exchange'

    def ready(self):
        import wagtail_block_exchange.signals  # noqa 