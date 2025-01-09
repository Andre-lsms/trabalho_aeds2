import struct

from faker import Faker

fake = Faker('pt_BR')


def escolher_registro(arquivo, entidade):
    quantidade = (tamanho_arquivo(arquivo) // tamanho_registro(entidade))
    posicao = fake.random_int(min=0, max=quantidade - 1)
    arquivo.seek((posicao * tamanho_registro(entidade)))
    registro_lido = entidade.ler_registro(arquivo)
    return registro_lido


def gerar_endereco():
    rua = fake.street_name()
    numero = fake.building_number()
    bairro = fake.bairro()
    cidade = fake.city()
    return rua + ', ' + numero + ' - ' + bairro + '. ' + cidade


def tamanho_arquivo(arquivo):
    arquivo.seek(0, 2)
    return arquivo.tell()


def tamanho_registro(entidade):
    return struct.calcsize(entidade.get_formato())
