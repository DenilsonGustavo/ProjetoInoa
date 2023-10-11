import os
import pandas as pd
from django.shortcuts import render
from io import StringIO
from .models import Cotacao, Ativo
import requests
import csv

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

def obter_cotacoes(request):
    # Chave de API Alpha Vantage
    api_key = 'XP3TZH661SLV08CX'

    # Consulta para obter todos os símbolos de Ativo
    ativos = Ativo.objects.values_list('simbolo', flat=True)

    # Lista de símbolos de empresas
    #simbolos_empresas = list(ativos)
    simbolos_empresas = ['ITUB4'] #, 'ABEV3', 'BBAS3'] # 'PETR4', 'VALE3' 'CVCB3', 'PCAR3', 'GOLL4', 'AZUL4', 'MGLU3']
    # Dataframe para armazenar as cotações obtidas
    df = pd.DataFrame()

    for simbolo in simbolos_empresas:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={simbolo}.SAO&apikey={api_key}&datatype=csv'
        #url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={simbolo}&apikey={api_key}&datatype=csv'
        r = requests.get(url)
        tabela = pd.read_csv(StringIO(r.text))
        lista_tabelas = [df, tabela]
        df = pd.concat(lista_tabelas)

    # Exclua todos os dados existentes no modelo Cotacao
    Cotacao.objects.all().delete()

    # Salve o dataframe em um arquivo CSV temporário
    df.to_csv('temp.csv', index=False)

    # Leia o arquivo CSV e salve os novos dados no banco de dados em uma única operação
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

    # Exclua o arquivo CSV temporário
    os.remove('temp.csv')

    context = {
        'cotacoes': cotacoes,
    }

    return render(request, 'ativos/cotacoes.html', context)

from .models import EmailEnviado  # Importe o modelo

def enviar_email(subject, message, from_email, recipient_list):
    # Envie o email

    # Após o envio bem-sucedido, salve a mensagem no banco de dados
    mensagem = EmailEnviado(
        assunto=subject,
        mensagem=message,
        de=from_email,
        para=recipient_list,
    )
    mensagem.save()

from .models import EmailEnviado
def monitorar_emails(request):
    # Exclua todos os dados existentes no modelo Cotacao
    EmailEnviado.objects.all().delete()
    ativos = Ativo.objects.all()
    for ativo in ativos:
        cotacoes = Cotacao.objects.filter(simbolo=ativo.simbolo)

        for cotacao in cotacoes:
            # Comparar os preços e tomar ação, por exemplo, enviar e-mails
            if cotacao.preco > ativo.limite_superior_tunnel:
                mensagem = f'Sugestão de venda para {ativo.simbolo}. Preço atual: {cotacao.preco}'
                enviar_email('Sugestão de Venda', mensagem, 'seuemail@gmail.com', ['emaildoinvestidor@gmail.com'])

            elif cotacao.preco < ativo.limite_inferior_tunnel:
                mensagem = f'Sugestão de compra para {ativo.simbolo}. Preço atual: {cotacao.preco}'
                enviar_email('Sugestão de Compra', mensagem, 'seuemail@gmail.com', ['emaildoinvestidor@gmail.com'])

    # Após enviar os emails, recupere os emails enviados
    emails_enviados = EmailEnviado.objects.all().order_by('-data_envio')
    print(emails_enviados)
    context = {
        'emails_enviados': emails_enviados,
    }

    return render(request, 'ativos/monitorar_emails.html', context)


