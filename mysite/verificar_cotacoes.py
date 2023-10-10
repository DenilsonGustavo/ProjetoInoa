import time
from polls.models import Ativo
from polls.models import Cotacao
import schedule

# Dicionário para rastrear o último tempo de verificação de cada ativo
ultima_verificacao = {}

# Função personalizada para simular o envio de e-mail, exibindo o conteúdo no terminal
def enviar_email(subject, message, from_email, recipient_list):
    print("Assunto:", subject)
    print("De:", from_email)
    print("Para:", recipient_list)
    print("Mensagem:")
    print(message)

# Função para verificar as condições e enviar e-mails
def verificar_cotacoes_e_enviar_email():
    global ultima_verificacao  # Permitir a modificação da variável global

    ativos = Ativo.objects.all()  # Obtém todos os ativos

    for ativo in ativos:
        cotacoes = Cotacao.objects.filter(simbolo=ativo.simbolo)  # Filtra as cotações pelo símbolo do ativo

        # Verifique o tempo decorrido desde a última verificação deste ativo
        tempo_atual = time.time()
        tempo_ultima_verificacao = ultima_verificacao.get(ativo.simbolo, 0)
        tempo_decorrido = tempo_atual - tempo_ultima_verificacao

        if tempo_decorrido >= (ativo.periodicidade_minutos * 60):
            for cotacao in cotacoes:
                # Comparar os preços e tomar ação, por exemplo, enviar e-mails
                if cotacao.preco > ativo.limite_superior_tunnel:
                    mensagem = f'Sugestao de venda para {ativo.simbolo}. Preco atual: {cotacao.preco}'
                    enviar_email('Sugestao de Venda', mensagem, 'seuemail@gmail.com', ['emaildoinvestidor@gmail.com'])

                elif cotacao.preco < ativo.limite_inferior_tunnel:
                    mensagem = f'Sugestao de compra para {ativo.simbolo}. Preco atual: {cotacao.preco}'
                    enviar_email('Sugestao de Compra', mensagem, 'seuemail@gmail.com', ['emaildoinvestidor@gmail.com'])

            # Atualize o último tempo de verificação para este ativo
            ultima_verificacao[ativo.simbolo] = tempo_atual

# Agende a verificação com o menor intervalo definido em Ativo.periodicidade_minutos
menor_intervalo = min(ativo.periodicidade_minutos for ativo in Ativo.objects.all())
schedule.every(menor_intervalo).minutes.do(verificar_cotacoes_e_enviar_email)

# Mantenha o script em execução
while True:
    schedule.run_pending()
    time.sleep(1)
