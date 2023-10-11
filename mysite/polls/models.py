from django.db import models

# Modelo para representar informações sobre ativos financeiros, como ações ou títulos
class Ativo(models.Model):
    objects = models.Manager()
    id_ativo = models.AutoField(primary_key=True)
    simbolo = models.CharField(max_length=10)  # Símbolo do ativo, por exemplo, "AAPL" para ações da Apple
    limite_inferior_tunnel = models.DecimalField(max_digits=10, decimal_places=2)  # Limite inferior do túnel de preço do ativo
    limite_superior_tunnel = models.DecimalField(max_digits=10, decimal_places=2)  # Limite superior do túnel de preço do ativo
    periodicidade_minutos = models.IntegerField()  # Periodicidade em minutos para monitorar o ativo

# Modelo para representar cotações de preços dos ativos
class Cotacao(models.Model):
    objects = models.Manager()
    id_cotacao = models.AutoField(primary_key=True)  # Chave estrangeira para o ativo associado à cotação
    simbolo = models.CharField(max_length=50)  # Símbolo do ativo (por exemplo, AAPL)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço mínimo
    high_price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço máximo
    open_price = models.DecimalField(max_digits=10, decimal_places=2)  # Preço de abertura
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Preço de abertura

class EmailEnviado(models.Model):
    objects = models.Manager()
    assunto = models.CharField(max_length=255)
    mensagem = models.TextField()
    de = models.EmailField()
    para = models.EmailField()
    data_envio = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.assunto


