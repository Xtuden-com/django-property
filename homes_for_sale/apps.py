from django.apps import AppConfig


class HomesForSaleConfig(AppConfig):
    name = 'homes_for_sale'
    verbose_name = 'Homes For Sale'

    def ready(self):
        import signals
