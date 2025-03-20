import os
import struct


def imprimir_todas_particoes(self):
    caminho = f'Bases/Particoes/{self._class.name_}'
    arquivos = os.listdir(caminho)
    quantidade = len(arquivos)
    for nome_arquivo in arquivos:
        if nome_arquivo.startswith('particao_') and nome_arquivo.endswith('.dat'):
            caminho_arquivo = os.path.join(caminho, nome_arquivo)
            with open(caminho_arquivo, 'r+b') as arquivo:
                print(f'Conteúdo da {nome_arquivo}: [{quantidade} ]')
                self.imprimir_codigos(arquivo)
                print()  # Linha em branco para separar as partições


from Entidades.clientes import Cliente
from Entidades.carro import Carro
from Entidades.filial import Filial
from Entidades.aluguel import Aluguel
from Entidades.tabela_hash import TabelaHashDisco
if not os.path.exists('Bases/hash'):
    os.makedirs('Bases/hash')
arquivo_lista = open('Bases/Hash/lista.dat', 'w+b')
arquivo_hash = open('Bases/Hash/tabela.dat', 'w+b')
arquivo_cliente = open('Bases/Cliente.dat', f'w+b')
arquivo_carro = open('Bases/Carro.dat', 'w+b')
arquivo_filial = open('Bases/Filial.dat', 'w+b')
arquivo = open('Bases/Aluguel.dat', 'w+b')
arquivo_log = open('Bases/Log2.txt', 'a+')

tam =10
clientes = Cliente()
carros = Carro()
filiais = Filial()
alugueis = Aluguel()
m = tam//10
clientes.criar_base(tam, arquivo=arquivo_cliente)
carros.criar_base(tam, arquivo=arquivo_carro)
filiais.criar_base(tam, arquivo=arquivo_filial)

tab_hash = TabelaHashDisco(tam, arquivo_hash,arquivo_lista)
alugueis.criar_base(tam, arquivo=arquivo, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                    arquivo_filial=arquivo_filial,tabela_hash=tab_hash)

# tab_hash.buscar(11)


alugueis.imprimir_base(arquivo)