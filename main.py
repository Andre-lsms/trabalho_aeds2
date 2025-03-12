import os
import struct


def imprimir_todas_particoes(self):
    caminho = f'Bases/Particoes/{self.__class__.__name__}'
    arquivos = os.listdir(caminho)
    quantidade = len(arquivos)
    for nome_arquivo in arquivos:
        if nome_arquivo.startswith('particao_') and nome_arquivo.endswith('.dat'):
            caminho_arquivo = os.path.join(caminho, nome_arquivo)
            with open(caminho_arquivo, 'r+b') as arquivo:
                print(f'Conteúdo da {nome_arquivo}: [{quantidade} ]')
                self.imprimir_codigos(arquivo)
                print()  # Linha em branco para separar as partições


import Funcoes.pesquiesa
from Entidades.clientes import Cliente
from Entidades.carro import Carro
from Entidades.filial import Filial
from Entidades.aluguel import Aluguel
from Funcoes.pesquiesa import *

arquivo_cliente = open('Bases/Cliente.dat', 'w+b')
arquivo_carro = open('Bases/Carro.dat', 'w+b')
arquivo_filial = open('Bases/Filial.dat', 'w+b')
arquivo = open('Bases/Aluguel.dat', 'w+b')
arquivo_cliente.seek(0)
arquivo_carro.seek(0)
arquivo_filial.seek(0)
arquivo.seek(0)
arquivo.write(struct.pack('i', -1))
arquivo_cliente.write(struct.pack('i', -1))
arquivo_carro.write(struct.pack('i', -1))
arquivo_filial.write(struct.pack('i', -1))

clientes = Cliente()
carros = Carro()
filiais = Filial()
alugueis = Aluguel()
tam = 100
m = tam // 10
clientes.criar_base(tam, arquivo=arquivo_cliente)
carros.criar_base(tam, arquivo=arquivo_carro)
filiais.criar_base(tam, arquivo=arquivo_filial)

alugueis.criar_base(tam, arquivo=arquivo, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                    arquivo_filial=arquivo_filial, )

clientes.ordenar_base(arquivo_cliente, m)
carros.ordenar_base(arquivo_carro, m)
filiais.ordenar_base(arquivo_filial, m)
alugueis.ordenar_base(arquivo, m)

clientes.imprimir_base(arquivo_cliente)
carros.imprimir_base(arquivo_carro)
filiais.imprimir_base(arquivo_filial)
alugueis.imprimir_base(arquivo)
