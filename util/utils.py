def formata_preco(preco):
    preco_formatado = f'R$ {preco:.2f} '.replace('.',',')
    return preco_formatado

def quantidade_produtos(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])


def valor_total(carrinho):
    total = 0
    for produto in carrinho.values():
        if produto['preco_quantitativo_promocional'] in carrinho:
            total += produto['preco_quantitativo_promocional']

        else:
            total += produto['preco_quantitativo']

    return total
