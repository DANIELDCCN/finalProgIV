from django.contrib import admin

from .models import Ternos, Atividade

@admin.register(Ternos)
class TernosAdmin(admin.ModelAdmin):
    list_display = ('nome','preco', 'ativo', 'modificado', 'imagem')



