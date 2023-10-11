from django.apps import AppConfig
from background_task.models import Task

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        if not Task.objects.filter(task_name='polls.tasks.atualizar_cotacoes_e_enviar_emails').exists():
            from mysite.polls.tasks import atualizar_cotacoes_e_enviar_emails
            atualizar_cotacoes_e_enviar_emails(repeat=60)  # Agende a função para ser executada repetidamente a cada 60 segundos
