from django.contrib import admin
from pedido.models import Pedido, ItemPedido


# Register your models here.

# @admin.register(ItemPedido)
class ItemPedidoInLine(admin.StackedInline):
    model = ItemPedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'total', 'status',
    ordering = '-id',
    search_fields = 'id', 'user', 'total', 'status',
    inlines = [
        ItemPedidoInLine
    ]