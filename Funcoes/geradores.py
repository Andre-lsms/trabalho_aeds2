import random

from Entidades.entidade_base import fake


def gerar_telefone_aleatorio():
    """Gera um número de telefone aleatório no formato brasileiro."""
    ddd = random.randint(11, 99)  # Gera um DDD válido (11 a 99)
    primeiro_digito = random.randint(6, 9)  # Celulares começam com 6, 7, 8 ou 9
    restantes = random.randint(1000000, 9999999)  # Gera os 7 dígitos restantes
    telefone = f"{ddd}{primeiro_digito}{restantes}"  # Monta o número completo
    return formatar_telefone(telefone)

def formatar_telefone(numero):
    """Formata um número de telefone brasileiro."""
    numero = ''.join(filter(str.isdigit, numero))  # Remove caracteres não numéricos
    if len(numero) == 11:  # Celular (11 dígitos)
        return f"({numero[:2]}) {numero[2:7]}-{numero[7:]}"
    elif len(numero) == 10:  # Telefone fixo (10 dígitos)
        return f"({numero[:2]}) {numero[2:6]}-{numero[6:]}"
    else:
        return "Número inválido"

def gerar_endereco():
    rua = fake.street_name()
    numero = fake.building_number()
    bairro = fake.bairro()
    cidade = fake.city()
    return rua + ', ' + numero + ' - ' + bairro + '. ' + cidade