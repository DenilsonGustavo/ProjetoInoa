from django.contrib import admin
from django.urls import path, include
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #rota, view responsável, nome de referência
    #meusite.com
    path('', views.index, name='index'),
    #meusite.com/ativos
    path('ativos/', views.ativos, name="listagem_ativos"),
    #excluir um ativo
    #path('excluir_ativo/<int:ativo_id>/', views.excluir_ativo, name='excluir_ativo'),
    path('cotacoes/', views.exibir_cotacoes, name='exibir_cotacoes'),
]