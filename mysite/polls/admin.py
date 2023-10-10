from django.contrib import admin
from .models import Ativo, Cotacao
# Register your models here.
admin.site.register(Ativo)
admin.site.register(Cotacao)