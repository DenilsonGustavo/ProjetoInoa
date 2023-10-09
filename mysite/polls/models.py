from django.db import models

# Create your models here.
from django.db import models

# Modelo para representar informações sobre ativos financeiros, como ações ou títulos
class Ativo(models.Model):
    id_ativo = models.AutoField(primary_key=True)
    simbolo = models.CharField(max_length=10)  # Símbolo do ativo, por exemplo, "AAPL" para ações da Apple
    limite_inferior_tunnel = models.DecimalField(max_digits=10, decimal_places=2)  # Limite inferior do túnel de preço do ativo
    limite_superior_tunnel = models.DecimalField(max_digits=10, decimal_places=2)  # Limite superior do túnel de preço do ativo
    periodicidade_minutos = models.IntegerField()  # Periodicidade em minutos para monitorar o ativo

# Modelo para representar cotações de preços dos ativos
class Cotacao(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE)  # Chave estrangeira para o ativo associado à cotação
    preco = models.DecimalField(max_digits=10, decimal_places=2)  # Preço da cotação
    data_hora = models.DateTimeField(auto_now_add=True)  # Data e hora em que a cotação foi registrada
