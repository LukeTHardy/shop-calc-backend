from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command


class CalcapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'calcapi'

    def ready(self):
        post_migrate.connect(run_recalculate_totalbf, sender=self)

def run_recalculate_totalbf(sender, **kwargs):
    call_command('recalculate_totalbf')
