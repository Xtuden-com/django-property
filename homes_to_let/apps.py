from django.apps import AppConfig


class HomesToLetConfig(AppConfig):
    name = 'homes_to_let'
    verbose_name = 'Homes To Let'

    def ready(self):
        import signals