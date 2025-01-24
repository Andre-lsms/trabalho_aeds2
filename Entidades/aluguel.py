import datetime
import random
import struct

from Entidades.carro import Carro
from Entidades.clientes import Cliente
from Entidades.entidade_base import EntidadeBase
from Entidades.filial import Filial
from Funcoes.sobrescrita import *

f_filiais = Filial()
c_clientes = Cliente()
c_carros = Carro()


class Aluguel(EntidadeBase):
    def __init__(self, codigo=0, id_cliente=0, nome_cliente=None, id_carro=0, diaria=0, id_filial=0,
                 data_aluguel=None, tempo=0, valor_total=0):
        super().__init__()
        self.codigo = codigo
        self.id_cliente = id_cliente
        self.nome_cliente = nome_cliente
        self.id_carro = id_carro
        self.diaria = diaria
        self.id_filial = id_filial
        self.data_aluguel = data_aluguel
        self.tempo = tempo
        self.valor_total = valor_total

    def criar_registro(self, codigo, **kwargs):
        carro = None
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        cliente = self.escolher_registro_aleatorio(arquivo_cliente, c_clientes)
        self.codigo = codigo
        self.id_cliente = cliente.codigo
        self.nome_cliente = cliente.nome

        for i in range(c_carros.quantidade_registros(arquivo_carro)):
            carro = self.escolher_registro_aleatorio(arquivo_carro, c_carros)
            if carro.disponivel:
                carro.disponivel = False
                sobrescrever(arquivo_carro, carro)
                break

        self.id_carro = carro.codigo
        filial = self.escolher_registro_aleatorio(arquivo_filial, f_filiais)
        self.id_filial = filial.codigo
        self.data_aluguel = self.fake.date_between(start_date='-30d', end_date='today')
        data_formatada = self.data_aluguel.strftime('%d/%m/%Y')
        self.diaria = self.fake.random_int(min=100, max=600)
        self.tempo =(datetime.date.today() - self.data_aluguel).days
        self.valor_total = self.diaria * self.tempo
        return Aluguel(
            codigo=self.codigo,
            id_cliente=self.id_cliente,
            nome_cliente=self.nome_cliente,
            id_carro=self.id_carro,
            id_filial=self.id_filial,
            data_aluguel=data_formatada,
            tempo=self.tempo,
            diaria=self.diaria,
            valor_total=self.valor_total
        )

    def salvar_registro(self, arquivo, registro):
        try:
            arquivo.write(struct.pack('i', registro.codigo))
            arquivo.write(struct.pack('i', registro.id_cliente))
            arquivo.write(struct.pack('30s', registro.nome_cliente.encode('utf-8')))
            arquivo.write(struct.pack('i', registro.id_carro))
            arquivo.write(struct.pack('i', registro.id_filial))
            arquivo.write(struct.pack('10s', registro.data_aluguel.encode('utf-8')))
            arquivo.write(struct.pack('i', registro.tempo))
            arquivo.write(struct.pack('i', registro.diaria))
            arquivo.write(struct.pack('i', registro.valor_total))
        except struct.error as e:
            print(f"Erro ao empacotar registro: {e}")

    def imprimir(self, registro):
        print(f'{95 * "_"}')
        print(f"Código: {registro.codigo}")
        print(f"ID Cliente: {registro.id_cliente}")
        print(f"Nome Cliente: {registro.nome_cliente.strip()}")
        print(f"ID Carro: {registro.id_carro}")
        print(f"ID Filial: {registro.id_filial}")
        print(f"Data do Aluguel: {registro.data_aluguel}")
        print(f"Tempo: {registro.tempo} Dias")
        print(f"Diária: R${registro.diaria}")
        print(f"Valor Total: R${registro.valor_total}")
        print(f'{96 * "_"}')

    def ler_registro(self, arquivo):
        try:
            registro_bytes = arquivo.read(self.tamanho_registro())
            if len(registro_bytes) < self.tamanho_registro():
                return None

            registro = struct.unpack(self.get_formato(), registro_bytes)
            cod, id_cliente, nome_cliente, id_carro, id_filial, data_aluguel, tempo, diaria, valor_total = registro
            return Aluguel(
                codigo=cod,
                id_cliente=id_cliente,
                nome_cliente=nome_cliente.decode('utf-8').rstrip(chr(0)),
                id_carro=id_carro,
                id_filial=id_filial,
                data_aluguel=data_aluguel.decode('utf-8').rstrip(chr(0)),
                diaria=diaria,
                tempo=tempo,
                valor_total=valor_total

            )
        except struct.error as e:
            print(f"Erro ao desempacotar registro: {e}")

    def criar_base(self, tamanho, **kwargs):
        arquivo = kwargs.get('arquivo')
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        if c_carros.quantidade_registros(arquivo_carro) < tamanho:
            raise ValueError("Não há carros suficientes para alugar")
        if arquivo is None:
            raise ValueError("O arquivo não foi informado")

        print(f'Gerando a base de daso tamanho {tamanho}...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        # shuffle(codigos)
        for i in range(len(codigos)):
            registro = self.criar_registro(codigo=codigos[i], arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                                          arquivo_filial=arquivo_filial)
            self.salvar_registro(arquivo, registro)

    def get_formato(self):
        return '=ii30sii10siii'

    def tamanho_registro(self):
        return int(struct.calcsize(self.get_formato()))

    @staticmethod
    def escolher_registro_aleatorio(arquivo, entidade):
        arquivo.seek(0)  # Garante que a leitura comece do início do arquivo
        tamanho_arquivo = entidade.tamanho_arquivo(arquivo)
        tamanho_registro = entidade.tamanho_registro()
        quant_registros = tamanho_arquivo // tamanho_registro
        posicao = random.randint(0, quant_registros - 1)
        arquivo.seek(posicao * tamanho_registro)
        registro_lido = entidade.ler_registro(arquivo)
        return registro_lido