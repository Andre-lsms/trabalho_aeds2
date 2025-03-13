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
arquivo_cliente = open('Bases/Cliente.dat', f'w+b')
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
arquivo_log = open('Bases/Log2.txt', 'a+')

clientes = Cliente()
carros = Carro()
filiais = Filial()
alugueis = Aluguel()
tam =100000
m = tam//10
clientes.criar_base(tam, arquivo=arquivo_cliente)
carros.criar_base(tam, arquivo=arquivo_carro)
filiais.criar_base(tam, arquivo=arquivo_filial)

alugueis.criar_base(tam, arquivo=arquivo, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                    arquivo_filial=arquivo_filial, )

# Copiar o arquivo de alugueis para fazer o buuble sort
arquivo.seek(0)
# arquivo_bubble = open('Bases/Aluguel_bubble.dat', 'w+b')
# arquivo_bubble.write(arquivo.read())
depuracao = False

selecao = alugueis.selecao_natural(arquivo ,m,depuracao=depuracao)
intercalacao = alugueis.intercalacao_otima( m,depuracao=depuracao)
# buuble = alugueis.bubble_sort(arquivo_bubble,depuracao=depuracao)


# Função para formatar o tempo para 2 casas decimais
def formatar_tempo(tempo):
    return round(tempo, 2)

# Exibindo os resultados com cores e tempo formatado

# Seleção Natural
print('\033[94mSeleção Natural:\033[0m')  # Azul
print(f'\033[96mNúmero de leituras:\033[0m {selecao[0]}')  # Ciano
print(f'\033[96mNúmero de escritas:\033[0m {selecao[1]}')  # Ciano
print(f'\033[92mTempo de execução:\033[0m {formatar_tempo(selecao[2])} segundos')  # Verde
print()

# Intercalação Ótima
print('\033[94mIntercalação Ótima:\033[0m')  # Azul
print(f'\033[96mNúmero de leituras:\033[0m {intercalacao[0]}')  # Ciano
print(f'\033[96mNúmero de escritas:\033[0m {intercalacao[1]}')  # Ciano
print(f'\033[92mTempo de execução:\033[0m {formatar_tempo(intercalacao[2])} segundos')  # Verde
print()

# Ordenação Externa por geração de partições
print('\033[94mOrdenação Externa por Geração de Partições:\033[0m')  # Azul
print(f'\033[96mNúmero de leituras:\033[0m {intercalacao[0] + selecao[0]}')  # Ciano
print(f'\033[96mNúmero de escritas:\033[0m {intercalacao[1] + selecao[1]}')  # Ciano
print(f'\033[92mTempo de execução:\033[0m {formatar_tempo(intercalacao[2] + selecao[2])} segundos')  # Verde
print()

# # Bubble Sort
# print('\033[94mBubble Sort:\033[0m')  # Azul
# print(f'\033[96mNúmero de leituras:\033[0m {buuble[0]}')  # Ciano
# print(f'\033[96mNúmero de escritas:\033[0m {buuble[1]}')  # Ciano
# print(f'\033[92mTempo de execução:\033[0m {formatar_tempo(buuble[2])} segundos')  # Verde
# print()


arquivo_log.write('\n')
arquivo_log.write(f'Base de dados com {tam} registros\n')
arquivo_log.write(f'Tamanho da memória: {m} ')
# Seleção Natural
arquivo_log.write('Seleção Natural:\n')  # Título sem cor
arquivo_log.write(f'Número de leituras: {selecao[0]}\n')  # Número de leituras
arquivo_log.write(f'Número de escritas: {selecao[1]}\n')  # Número de escritas
arquivo_log.write(f'Tempo de execução: {formatar_tempo(selecao[2])} segundos\n\n')  # Tempo de execução

# Intercalação Ótima
arquivo_log.write('Intercalação Ótima:\n')  # Título sem cor
arquivo_log.write(f'Número de leituras: {intercalacao[0]}\n')  # Número de leituras
arquivo_log.write(f'Número de escritas: {intercalacao[1]}\n')  # Número de escritas
arquivo_log.write(f'Tempo de execução: {formatar_tempo(intercalacao[2])} segundos\n\n')  # Tempo de execução

# Ordenação Externa por geração de partições
arquivo_log.write('Ordenação Externa por Geração de Partições:\n')  # Título sem cor
arquivo_log.write(f'Número de leituras: {intercalacao[0] + selecao[0]}\n')  # Total de leituras
arquivo_log.write(f'Número de escritas: {intercalacao[1] + selecao[1]}\n')  # Total de escritas
arquivo_log.write(f'Tempo de execução: {formatar_tempo(intercalacao[2] + selecao[2])} segundos\n\n')  # Tempo total

# # Bubble Sort
# arquivo_log.write('Bubble Sort:\n')  # Título sem cor
# arquivo_log.write(f'Número de leituras: {buuble[0]}\n')  # Número de leituras
# arquivo_log.write(f'Número de escritas: {buuble[1]}\n')  # Número de escritas
# arquivo_log.write(f'Tempo de execução: {formatar_tempo(buuble[2])} segundos\n\n')  # Tempo de execução
