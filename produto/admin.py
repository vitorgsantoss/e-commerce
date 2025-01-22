from django.contrib import admin
from produto.models import Produto, Variacao

# Register your models here.
class VariacaoInLine(admin.TabularInline):
    model = Variacao
    extra = 1 


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [
        VariacaoInLine
    ]
    list_display = (
    'id', 'nome','descricao_curta', 'preco_marketing', 'preco_marketing_promocional', 'tipo',
    )
    list_display_links = 'id', 'nome'
    ordering = '-id',
    search_fields = 'id', 'nome', 'descricao_curta', 'tipo',
    prepopulated_fields = {
        'slug': ('nome',),
    }


    
