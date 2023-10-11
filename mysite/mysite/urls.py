from django.contrib import admin
from django.urls import path, include
from .polls import views

urlpatterns = [
    path('polls/',include('polls.urls')),
    path('admin/', admin.site.urls),
    #rota, view responsável, nome de referência
    #meusite.com
    path('', views.home, name='home'),
    path('cadastro/', views.index, name='index'),
    #meusite.com/ativos
    path('ativos/', views.ativos, name="listagem_ativos"),
    path('cotacoes/', views.obter_cotacoes, name='exibir_cotacoes'),
    path('monitorar_emails/', views.monitorar_emails, name='monitorar_emails'),
]