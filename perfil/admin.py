from django.contrib import admin
from perfil.models import Perfil, Endereco


class EnderecoInLine(admin.StackedInline):
    model = Endereco
    extra = 1

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = 'usuario', 'cpf',
    inlines = [
        EnderecoInLine
    ]
