import requests
from .models import Cotacao

def buscar_cotacoes(ativo):
    api_key = 'XP3TZH661SLV08CX'
    symbol = ativo.simbolo  # Supondo que simbolo seja o símbolo do ativo

    # Construa a URL da API com seu símbolo e sua chave de API
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={api_key}'

    try:
        response = requests.get(url)
        data = response.json()
        time_series = data.get('Time Series (1min)')

        for timestamp, values in time_series.items():
            price = values.get('1. open')
            cotacao = Cotacao(ativo=ativo, preco=price)
            cotacao.save()

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar cotações para {symbol}: {str(e)}")

# Chame essa função passando um objeto Ativo para buscar as cotações e armazená-las no banco de dados
