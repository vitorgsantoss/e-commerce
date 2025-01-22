def validate(cpf):
    cpf = cpf.translate(str.maketrans('', '', '.-'))

    if len(cpf) != 11 or not cpf.isdigit() or len(set(cpf)) == 1:
        return False

    cpf_separado = [int(x) for x in cpf]

    def calcular_digito(cpf, peso_inicial):
        soma = sum(cpf[i] * (peso_inicial - i) for i in range(peso_inicial - 1))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    primeiro_digito = calcular_digito(cpf_separado, 10)
    if primeiro_digito != cpf_separado[9]:
        return False

    segundo_digito = calcular_digito(cpf_separado, 11)
    if segundo_digito != cpf_separado[10]:
        return False

    return True

