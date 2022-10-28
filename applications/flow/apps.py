from django.apps import AppConfig
from django.db.models.signals import post_migrate


class FlowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.flow'

    def ready(self):
        from applications.flow.handlers import init_node_template
        post_migrate.connect(init_node_template, self)
