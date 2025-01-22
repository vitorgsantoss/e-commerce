from django.template import Library
from util import utils

register = Library()

@register.filter
def formata_preco(preco):
    return utils.formata_preco(preco)