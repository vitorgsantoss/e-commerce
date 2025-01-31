from django.template import Library
from util import utils

register = Library()

@register.filter
def formata_preco(preco):
    return utils.formata_preco(preco)

@register.filter
def quantidade_produtos(carrinho):
    return utils.quantidade_produtos(carrinho)

@register.filter
def valor_total(carrinho):
    return utils.valor_total(carrinho)