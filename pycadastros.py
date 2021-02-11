import re
from random import randint

def isValidCPF(cpf, fill=False):
    if fill:
        cpfTuple = formatCPF(cpf)
        cpf = cpfTuple[1]

    cpfLista = [int(char) for char in str(cpf)]
    cpfMod = [cpfLista[len(cpfLista) - 2], cpfLista[len(cpfLista) - 1]]

    if len(cpfLista) == 11:
        cpfLista.pop()
        cpfLista.pop()

        # Primeira verificação
        soma = 0
        for index, digito in enumerate(cpfLista):
            i = 10 - index
            soma += i * digito

        soma *= 10
        resto = soma % 11

        if resto == 10:
            resto = 0

        if resto == cpfMod[0]:
            # Segunda verificação
            cpfLista.append(cpfMod[0])

            soma = 0
            for index, digito in enumerate(cpfLista):
                i = 11 - index
                soma += i * digito

            soma *= 10
            resto = soma % 11

            if resto == 10:
                resto = 0

            if resto == cpfMod[1]:
                return True

        return False


def isValidCNPJ(cnpj, fill=False):
    if fill:
        cnpjTuple = formatCNPJ(cnpj)
        cnpj = cnpjTuple[1]

    cnpjValores = [(5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2),
                   (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)]

    cnpj = re.sub(r"\D", "", str(cnpj))
    cadastro = cnpj[:12]
    digitos = [int(cnpj[12]), int(cnpj[13])]

    soma = 0
    for i in range(len(cadastro)):
        soma = soma + int(cadastro[i]) * cnpjValores[0][i]

    resto = soma % 11
    if resto < 2:
        resto = 0
    else:
        resto = 11 - resto

    if resto == digitos[0]:
        soma = 0
        for i in range(len(cadastro)):
            soma = soma + int(cadastro[i]) * cnpjValores[1][i]

        resto = soma % 11
        if resto < 2:
            resto = 0
        else:
            resto = 11 - resto

        if resto == digitos[1]:
            return True

    return False


def formatCPF(cpf):
    cpf = re.sub(r"\D", "", str(cpf))
    cpf = str(cpf)
    cpfLista = [str(char) for char in cpf]

    nLeadingZeros = 11 - len(cpfLista)
    for n in range(nLeadingZeros):
        cpfLista.insert(0, '0')

    cpfNum = str(''.join(cpfLista))
    cpfLista.insert(3, '.')
    cpfLista.insert(7, '.')
    cpfLista.insert(11, '-')
    cpfStr = ''.join(cpfLista)

    return int(cpfNum), cpfNum, cpfStr, 'CPF'


def formatCNPJ(cnpj):
    cnpj = re.sub(r"\D", "", str(cnpj))
    cnpj = str(cnpj)
    cnpjLista = [str(char) for char in cnpj]

    nLeadingZeros = 14 - len(cnpjLista)
    for n in range(nLeadingZeros):
        cnpjLista.insert(0, '0')

    cnpjNum = str(''.join(cnpjLista))
    cnpjLista.insert(2, '.')
    cnpjLista.insert(6, '.')
    cnpjLista.insert(10, '/')
    cnpjLista.insert(13, '-')
    cnpjStr = ''.join(cnpjLista)

    return int(cnpjNum), cnpjNum, cnpjStr, 'CNPJ'


def formatCadastro(cadastro):
    if tipoCadastro(cadastro) == 'CPF':
        cpf = formatCPF(cadastro)
        return cpf

    elif tipoCadastro(cadastro) == 'CNPJ':
        cnpj = formatCNPJ(cadastro)
        return cnpj

    else:
        return None


def tipoCadastro(cadastro):
    # Testar se é CNPJ
    cadastro = re.sub(r"\D", "", str(cadastro))
    cadastroLista = [str(char) for char in cadastro]

    nLeadingZeros = 14 - len(cadastroLista)
    for n in range(nLeadingZeros):
        cadastroLista.insert(0, '0')
    cnpj = ''.join(cadastroLista)
    canBeCNPJ = isValidCNPJ(cnpj)

    # Testar se é CPF
    cadastro = re.sub(r"\D", "", str(cadastro))
    cadastroLista = [str(char) for char in cadastro]

    nLeadingZeros = 11 - len(cadastroLista)
    for n in range(nLeadingZeros):
        cadastroLista.insert(0, '0')
    cpf = ''.join(cadastroLista)
    canBeCPF = isValidCPF(cpf)

    if canBeCNPJ and canBeCPF:
        return None

    else:
        if canBeCNPJ:
            return 'CNPJ'

        elif canBeCPF:
            return 'CPF'

        else:
            return None


def excelFormatCadastro(cadastro, workbook, validate=False):
    # Recebe um pd.ExcelWriter.book
    if validate:
        if tipoCadastro(cadastro) == 'CPF':
            if isValidCPF(cadastro):
                cadastroFormat = workbook.add_format({'num_format': '000.000.000-00'})

            else:
                return None

        elif tipoCadastro(cadastro) == 'CNPJ':
            if isValidCNPJ(cadastro):
                cadastroFormat = workbook.add_format({'num_format': '00.000.000/0000-00'})
            else:
                return None

        else:
            return None



    else:

        if tipoCadastro(cadastro) == 'CPF':

            cadastroFormat = workbook.add_format({'num_format': '000.000.000-00'})



        elif tipoCadastro(cadastro) == 'CNPJ':

            cadastroFormat = workbook.add_format({'num_format': '00.000.000/0000-00'})



        else:

            return None

    return cadastroFormat


def generateCPF(mask=False, leadingZeros=True):
    if leadingZeros:
        cpf = randint(0, 999999999)
        cpf = str(cpf)
        cpfLista = [str(char) for char in cpf]

        nLeadingZeros = 9 - len(cpfLista)
        for n in range(nLeadingZeros):
            cpfLista.insert(0, '0')

    else:
        cpf = randint(100000000, 999999999)
        cpfLista = [str(char) for char in str(cpf)]

    soma = 0
    for index, digito in enumerate(cpfLista):
        i = 10 - index
        soma += i * int(digito)

    soma *= 10
    resto = soma % 11

    if resto == 10:
        resto = 0

    cpfLista.append(str(resto))

    soma = 0
    for index, digito in enumerate(cpfLista):
        i = 11 - index
        soma += i * int(digito)

    soma *= 10
    resto = soma % 11

    if resto == 10:
        resto = 0

    cpfLista.append(str(resto))
    cpf = ''.join(cpfLista)

    if mask:
        cpf = formatCPF(cpf)[2]

    return cpf


def generateCNPJ(mask=False, leadingZeros=True):
    cnpjValores = [(5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2),
                   (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)]

    if leadingZeros:
        cnpj = str(randint(0, 999999999999))
        cnpjLista = [str(char) for char in cnpj]

        nLeadingZeros = 12 - len(cnpjLista)
        for n in range(nLeadingZeros):
            cnpjLista.insert(0, '0')

    else:
        cnpj = randint(100000000000, 999999999999)
        cnpjLista = [str(char) for char in str(cnpj)]

    soma = 0
    for valor, digito in zip(cnpjValores[0], cnpjLista):
        soma += valor * int(digito)

    soma *= 10
    resto = soma % 11

    if resto < 2 or resto == 10:
        resto = 0

    else:
        resto = 11 - resto

    cnpjLista.append(str(resto))

    soma = 0
    for valor, digito in zip(cnpjValores[1], cnpjLista):
        soma += valor * int(digito)

    soma *= 10
    resto = soma % 11

    if resto < 2 or resto == 10:
        resto = 0

    else:
        resto = 11 - resto

    cnpjLista.append(str(resto))
    cnpj = ''.join(cnpjLista)

    if mask:
        cnpj = formatCNPJ(cnpj)[2]

    return cnpj

# TESTES PRA VALIDAÇÃO DE CNPJ
# -----------------------------
# 00080671000100
# 03279571000103
# 40362607000136
# -----------------------------

