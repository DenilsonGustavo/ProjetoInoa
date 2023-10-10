from django.shortcuts import render
from .models import Ativo
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from django.shortcuts import render
from io import StringIO
from .models import Cotacao
import requests
from django.utils import timezone
from .utils import buscar_cotacoes  # Importa função criada
import csv
from IPython.display import display
from csv import writer, reader

def index(request):
    return render(request, 'ativos/index.html')

def home(request):
    return render(request, 'ativos/home.html')

def ativos(request):
    if request.method == 'POST':
        # Obtenha os dados do formulário POST
        simbolo = request.POST.get('simbolo')
        limite_inferior_tunnel = request.POST.get('limite_inferior_tunnel')
        limite_superior_tunnel = request.POST.get('limite_superior_tunnel')
        periodicidade_minutos = request.POST.get('periodicidade')

        # Crie um novo objeto Ativo e salve-o no banco de dados
        novo_ativo = Ativo(
            simbolo=simbolo,
            limite_inferior_tunnel=limite_inferior_tunnel,
            limite_superior_tunnel=limite_superior_tunnel,
            periodicidade_minutos=periodicidade_minutos
        )
        novo_ativo.save()

    # Consulte todos os ativos já cadastrados
    ativos_cadastrados = Ativo.objects.all()

    # Passe os ativos para o template
    ativos = {'ativos': ativos_cadastrados}

    # Renderize a página de ativos
    return render(request, 'ativos/ativos.html', ativos)

from datetime import datetime

def obter_cotacoes(request):
    # Chave de API Alpha Vantage
    api_key = 'XP3TZH661SLV08CX'

    # Lista de símbolos de empresas
    simbolos_empresas = ['ITUB4', 'ABEV3', 'BBAS3']

    # Dataframe para armazenar as cotações obtidas
    df = pd.DataFrame()

    for simbolo in simbolos_empresas:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={simbolo}.SAO&apikey={api_key}&datatype=csv'
        r = requests.get(url)
        tabela = pd.read_csv(StringIO(r.text))
        lista_tabelas = [df, tabela]
        df = pd.concat(lista_tabelas)

        #display(df)
    # Salve o dataframe em um arquivo CSV temporário
    df.to_csv('temp.csv', index=False)
    # Leia o arquivo CSV e salve os dados no banco de dados em uma única operação
    with open('temp.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # pule a linha do cabeçalho
        for row in reader:
            # Crie uma instância de Cotacao com os dados
            cotacao = Cotacao(
                simbolo=row[0],
                open_price=row[1],
                low_price=row[3],
                high_price=row[2],
                preco=row[4],
            )
            # Salve a instância no banco de dados
            cotacao.save()

    # Recupere todas as cotações do banco de dados
    cotacoes = Cotacao.objects.all()

    # Mostre os valores das cotações inseridas
    for cotacao in cotacoes:
        print(f"Simbolo: {cotacao.simbolo}, Lower price: {cotacao.low_price}, Higher price: {cotacao.high_price}")

    context = {
        'cotacoes': cotacoes,
    }

    return render(request, 'ativos/cotacoes.html', context)
