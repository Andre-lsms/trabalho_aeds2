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
        return '=i34s34si34s34s'

    def criar_registro(self, cod, **kwargs):
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')

        arquivo_filial = kwargs.get('arquivo_filial')
        codigo = cod
        cliente = (funcoes.escolher_registro(arquivo_cliente, clientes))[:34]
        carro = (funcoes.escolher_registro(arquivo_carro, carros))[:34]
        diaria = self.fake.random_int(min=100, max=1000)
        filial_aluguel = (funcoes.escolher_registro(arquivo_filial, filiais))[:34]
        filial_devolucao = (funcoes.escolher_registro(arquivo_filial, filiais))[:34]

        return codigo, cliente[0], cliente[1], carro[0], carro[
            1], diaria, f'[{filial_aluguel[0]}] {filial_aluguel[1]}', f'[{filial_devolucao[0]}] {filial_devolucao[1]}'

    def imprimir_registro(self, registro):
        registro_lido = self.ler_registro(registro)
        if registro_lido[0] is None:
            return
        print(f"Codigo: [{registro_lido[0]}]")
        print(f"Cliente: {registro_lido[1]}")
        print(f"Carro: {registro_lido[2]}")
        print(f"Diaria: {registro_lido[3]}")
        print(f"Filial de Aluguel: {registro_lido[4]}")
        print(f"Filial de Devolucao: {registro_lido[5]}")
        print(f'{80 * "-"}')

    def criar_base(self, tamanho, **kwargs):
        arquivo_aluguel = kwargs.get('arquivo_aluguel')
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        print(f'Gerando {tamanho} registros...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        for i in codigos:
            registro_criado = (self.criar_registro(i, arquivo_aluguel=arquivo_aluguel, arquivo_cliente=arquivo_cliente,
                                                   arquivo_carro=arquivo_carro, arquivo_filial=arquivo_filial))
            self.salvar_registro(arquivo=arquivo_aluguel, registro=registro_criado)
