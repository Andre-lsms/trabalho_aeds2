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
        return '=ii30s14si7s30s30sii30s'

    def criar_registro(self, cod, id_cliente=None, id_carro=None, id_filial=None, diaria=0, **kwargs):
        global id_filia_aluguel, cpf_cliente, modelo_carro, marca_carro, placa_carro, nome_cliente, nome_filial_aluguel
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        codigo = cod

        if id_cliente is None:
            cliente = (funcoes.escolher_registro(arquivo_cliente, clientes))
            id_cliente = cliente[0]
            nome_cliente = cliente[1]
            cpf_cliente = cliente[3]

        if id_carro is None:
            carro = (funcoes.escolher_registro(arquivo_carro, carros))
            id_carro = carro[0]
            placa_carro = carro[1]
            marca_carro = carro[2]
            modelo_carro = carro[3]
        if diaria == 0:
            diaria = self.fake.random_int(min=100, max=1000)
        else:
            diaria = diaria
        if id_filial is None:
            filial_aluguel = (funcoes.escolher_registro(arquivo_filial, filiais))
            id_filia_aluguel = filial_aluguel[0]
            nome_filial_aluguel = filial_aluguel[1]

        return (codigo, id_cliente, nome_cliente, cpf_cliente, id_carro,placa_carro, marca_carro, modelo_carro,  diaria,
                id_filia_aluguel, nome_filial_aluguel)

    def imprimir_registro(self, registro, saida):
        saida.write(f"Codigo: [{registro[0]}]")
        saida.write(f"Cliente: [{registro[1]}] {registro[2].decode('utf-8').rstrip(chr(0))}")
        saida.write(
            f"Carro: [{registro[4]}] {registro[5].decode('utf-8').rstrip(chr(0))} - {registro[6].decode('utf-8').rstrip(chr(0))}")
        saida.write(f"Diaria: R$ {registro[8]}")
        saida.write(f"Filial de Aluguel: [{registro[9]}] {registro[10].decode('utf-8').rstrip(chr(0))}")
        saida.write(f'{95 * "_"}')

    def criar_base(self, tamanho, desordenada=True, **kwargs):
        arquivo_aluguel = kwargs.get('arquivo')
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        arquivo_log = kwargs.get('arquivo_log')
        print(f'Gerando {tamanho} registros...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        if desordenada:
            shuffle(codigos)
        for i in codigos:
            registro_criado = (self.criar_registro(i, arquivo_cliente=arquivo_cliente,
                                                   arquivo_carro=arquivo_carro, arquivo_filial=arquivo_filial,
                                                   arquivo_log=arquivo_log))
            self.salvar_registro(arquivo=arquivo_aluguel, registro=registro_criado)
