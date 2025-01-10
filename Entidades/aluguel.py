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

    @classmethod
    def get_formato(cls):
        # Define o formato do registro para Aluguel
        return '=ii30si30s30sii30si30s'

    def criar_registro(self, cod, **kwargs):
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')

        arquivo_filial = kwargs.get('arquivo_filial')
        codigo = cod
        cliente = (funcoes.escolher_registro(arquivo_cliente, clientes))[:34]
        id_cliente = cliente[0]
        nome_cliente = cliente[1]
        carro = (funcoes.escolher_registro(arquivo_carro, carros))[:34]
        id_carro = carro[0]
        modelo_carro = carro[1]
        marca_carro = carro[3]
        diaria = self.fake.random_int(min=100, max=1000)
        filial_aluguel = (funcoes.escolher_registro(arquivo_filial, filiais))[:34]
        id_filia_aluguel = filial_aluguel[0]
        nome_filial_aluguel = filial_aluguel[1]
        filial_devolucao = (funcoes.escolher_registro(arquivo_filial, filiais))[:34]
        id_filial_devolucao = filial_devolucao[0]
        nome_filial_devolucao = filial_devolucao[1]
        return codigo, id_cliente, nome_cliente, id_carro, modelo_carro,marca_carro, diaria, id_filia_aluguel, nome_filial_aluguel, id_filial_devolucao, nome_filial_devolucao

    def imprimir_registro(self, registro):
        print(f"Codigo: [{registro[0]}]")
        print(f"Cliente: [{registro[1]}] {registro[2].decode('utf-8').rstrip(chr(0))}")
        print(f"Carro: [{registro[3]}] {registro[4].decode('utf-8').rstrip(chr(0))} - {registro[5].decode('utf-8').rstrip(chr(0))}")
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
