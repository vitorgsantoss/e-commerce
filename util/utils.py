def formata_preco(preco):
    preco_formatado = f'R$ {preco:.2f} '.replace('.',',')
    return preco_formatado