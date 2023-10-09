from django.shortcuts import render
from .models import Ativo
from .models import Cotacao
import requests
from .utils import buscar_cotacoes  # Importa função criada

def index(request):
    return render(request, 'ativos/index.html')


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

def atualizar_cotacoes(request, ativo_id):
    ativo = Ativo.objects.get(pk=ativo_id)
    buscar_cotacoes(ativo)
    return render(request, 'sucesso.html')  # Crie uma página "sucesso" para exibir uma mensagem após a atualização

def exibir_cotacoes(request):
    cotacoes = Cotacao.objects.all().order_by('-data_hora')  # Obtém todas as cotações, ordenadas pela data e hora mais recente
    return render(request, 'ativos/cotacoes.html', {'cotacoes': cotacoes})
