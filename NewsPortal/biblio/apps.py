from django.apps import AppConfig

class BiblioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'biblio'
    verbose_name = 'Новостной портал'  # Добавляем человекочитаемое название для админки

    def ready(self):
        import biblio.signals