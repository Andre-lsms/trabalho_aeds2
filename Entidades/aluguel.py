import random
from random import shuffle

from Entidades.entidade_base import EntidadeBase
from Entidades import funcoes
from Entidades.filial import Filial
from Entidades.clientes import Cliente
from Entidades.carro import Carro

filiais = Filial()
clientes = Cliente()
carros = Carro()


class Aluguel(EntidadeBase):
    def __init__(self, cod=0, cliente=None, carro=None, diaria=0, filial_aluguel=None,data_aluguel=None,
                 filial_devolucao=None,data_devolucao=None):
        super().__init__()
        self.codigo = cod
        self.cliente = cliente
        self.carro = carro
        self.diaria = diaria
        self.filial_aluguel = filial_aluguel
        self.data_aluguel = data_aluguel
        self.filial_devolucao = filial_devolucao
        self.data_devolucao = data_devolucao


    def criar_registro(self, codigo, **kwargs):
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        self.codigo = codigo


    def imprimir_registro(self, registro):
        print(f"Codigo: [{registro[0]}]")
        print(f"Cliente: [{registro[1]}] {registro[2].decode('utf-8').rstrip(chr(0))}")
        print(
            f"Carro: [{registro[3]}] {registro[4].decode('utf-8').rstrip(chr(0))} - {registro[5].decode('utf-8').rstrip(chr(0))}")
        print(f"Diaria: R$ {registro[6]}")
        print(f"Filial de Aluguel: [{registro[7]}] {registro[8].decode('utf-8').rstrip(chr(0))}")
        print(f"Filial de Devolucao: [{registro[9]}] {registro[10].decode('utf-8').rstrip(chr(0))}")
        print(80 * '-')

    def criar_base(self, tamanho, **kwargs):
        arquivo_aluguel = kwargs.get('arquivo_aluguel')
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        print(f'Gerando {tamanho} registros...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        shuffle(codigos)
        for i in codigos:
            registro_criado = (self.criar_registro(i, arquivo_aluguel=arquivo_aluguel, arquivo_cliente=arquivo_cliente,
                                                   arquivo_carro=arquivo_carro, arquivo_filial=arquivo_filial))
            self.salvar_registro(arquivo=arquivo_aluguel, registro=registro_criado)

    def get_formato(self):
        # Define o formato do registro para Aluguel
        return '=ii30si30s30sii30si30s'

    def escolher_registro_aleatorio(self,arquivo,entidade):
        tamanho = entidade.tamanho_arquivo(arquivo)
        quant_arquivos = tamanho // entidade.tamanho_registro()
        posicao = random.randint(0,quant_arquivos-1)
        arquivo.seek(posicao*entidade.tamanho_registro)
        return entidade.ler_registro(arquivo)
