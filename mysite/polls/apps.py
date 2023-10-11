
from django.apps import AppConfig

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

"""
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from background_task.models import Task
class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
    def ready(self):
        post_migrate.connect(self.schedule_background_task, sender=self)
    def schedule_background_task(self, sender, **kwargs):
        # Verifique se a tarefa já está agendada
        if not Task.objects.filter(task_name='polls.tasks.atualizar_cotacoes_e_enviar_emails').exists():
            from background_task import background
            from .tasks import atualizar_cotacoes_e_enviar_emails

            # Agende a função para ser executada repetidamente a cada 60 segundos
            background(atualizar_cotacoes_e_enviar_emails, schedule=60)
"""
