from datetime import datetime, timedelta
import pandas as pd
from io import StringIO
import requests
from celery import shared_task
from .models import Cotacao, Ativo, EmailEnviado
from .views import monitorar_emails,enviar_email  # Importe a função monitorar_emails
from .models import EmailEnviado

@shared_task
def atualizar_cotacoes_e_enviar_emails():
    # Obtenha a hora atual
    agora = datetime.now()
    api_key = 'XP3TZH661SLV08CX'
    # Consulte todos os ativos cadastrados
    ativos = Ativo.objects.all()

    for ativo in ativos:
        # Verifique se já é hora de atualizar com base na periodicidade do ativo
        tempo_desde_ultima_atualizacao = (agora - ativo.data_ultima_atualizacao).total_seconds()
        if tempo_desde_ultima_atualizacao >= (ativo.periodicidade_minutos * 60):
            # Atualize apenas este ativo
            # Consulte a cotação atual do ativo usando a API Alpha Vantage
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ativo.simbolo}.SAO&apikey={api_key}&datatype=csv'
            r = requests.get(url)
            tabela = pd.read_csv(StringIO(r.text))

            # Verifique se a tabela está vazia ou se não contém a informação necessária
            if not tabela.empty and '05. price' in tabela.columns:
                # Obtenha a cotação mais recente
                cotacao_atual = tabela['05. price'].iloc[0]

                # Atualize os dados no modelo Cotacao para este ativo
                cotacao = Cotacao(
                    simbolo=ativo.simbolo,
                    open_price=tabela['02. open'].iloc[0],
                    low_price=tabela['04. low'].iloc[0],
                    high_price=tabela['03. high'].iloc[0],
                    preco=cotacao_atual
                )

                # Salve a instância no banco de dados
                cotacao.save()

                # Atualize a data da última atualização para o ativo
                ativo.data_ultima_atualizacao = agora
                ativo.save()

                # Agora, chame a view monitorar_emails diretamente com o contexto apropriado
                monitorar_emails()

