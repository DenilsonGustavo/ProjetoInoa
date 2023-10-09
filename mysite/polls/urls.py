from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ativos/', views.ativos, name="listagem_ativos")
]
