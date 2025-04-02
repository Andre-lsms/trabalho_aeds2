import datetime
import random
import struct

from Entidades.carro import Carro
from Entidades.clientes import Cliente
from Entidades.entidade_base import EntidadeBase
from Entidades.filial import Filial

f_filiais = Filial()
c_clientes = Cliente()
c_carros = Carro()


class Aluguel(EntidadeBase):

    def __init__(self, ocupado=True, proximo=-1, codigo=0, cliente: Cliente = None, carro: Carro = None,
                 filial: Filial = None,
                 diaria=0,
                 data_aluguel=None, tempo=0, valor_total=0, ):
        super().__init__()
        self.nome_classe = 'Aluguel'
        self.ocupado = ocupado
        self.proximo = proximo
        self.codigo = codigo
        self.cliente = cliente
        self.carro = carro
        self.filial = filial
        self.diaria = diaria
        self.data_aluguel = data_aluguel
        self.tempo = tempo
        self.valor_total = valor_total

    def ler_topo_pilha(self, arquivo):
        arquivo.seek(0)
        return struct.unpack('i', arquivo.read(4))[0]

    def escrever_topo_pilha(self, arquivo, rrn):
        arquivo.seek(0)
        arquivo.write(struct.pack('i', rrn))

    def salvar_registro(self, arquivo, registro):
        try:
            posicao = arquivo.tell()
            arquivo.write(struct.pack('?', registro.ocupado))
            arquivo.write(struct.pack('i', registro.proximo))
            arquivo.write(struct.pack('i', registro.codigo))
            arquivo.write(struct.pack('i', registro.cliente.codigo))
            arquivo.write(struct.pack('30s', registro.cliente.nome.encode('utf-8')))
            arquivo.write(struct.pack('i', registro.carro.codigo))
            arquivo.write(struct.pack('i', registro.filial.codigo))
            arquivo.write(struct.pack('10s', registro.data_aluguel.encode('utf-8')))
            arquivo.write(struct.pack('i', registro.tempo))
            arquivo.write(struct.pack('i', registro.diaria))
            arquivo.write(struct.pack('i', registro.valor_total))
        except struct.error as e:
            print(f"Erro ao empacotar registro: {e}")

    def criar_registro(self, codigo, **kwargs):
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        self.cliente = kwargs.get('cliente')
        self.carro = kwargs.get('carro')
        self.filial = kwargs.get('filial')
        self.data_aluguel = kwargs.get('data_aluguel')
        self.diaria = kwargs.get('diaria')
        self.tempo = kwargs.get('tempo')

        if self.cliente is None:
            self.cliente = self.escolher_registro_aleatorio(arquivo_cliente, c_clientes)
        self.codigo = codigo

        if self.carro is None:
            while True:
                self.carro = self.escolher_registro_aleatorio(arquivo_carro, c_carros)
                if self.carro.disponivel:
                    break
        self.carro.disponivel = False
        self.carro.sobrescrever(arquivo_carro, self.carro)

        if self.filial is None:
            self.filial = self.escolher_registro_aleatorio(arquivo_filial, f_filiais)

        if self.diaria is None:
            self.diaria = self.fake.random_int(min=100, max=600)
        if self.data_aluguel is None:
            data = self.fake.date_between(start_date='-30d', end_date='today')
            self.data_aluguel = data.strftime('%d/%m/%Y')
        if self.tempo is None:
            self.tempo = (datetime.date.today() - datetime.datetime.strptime(self.data_aluguel, "%d/%m/%Y").date()).days
        self.valor_total = self.diaria * self.tempo

        return Aluguel(
            codigo=self.codigo,
            cliente=self.cliente,
            carro=self.carro,
            filial=self.filial,
            data_aluguel=self.data_aluguel,
            tempo=self.tempo,
            diaria=self.diaria,
            valor_total=self.valor_total
        )

    def imprimir(self, registro):

        print(f'{95 * "_"}')
        print(f"Código: {registro.codigo}")
        print(f"ID Cliente: {registro.cliente.codigo}")
        print(f"Nome Cliente: {registro.cliente.nome.strip()}")
        print(f"ID Carro: {registro.carro.codigo}")
        print(f"ID Filial: {registro.filial.codigo}")
        print(f"Data do Aluguel: {registro.data_aluguel}")
        print(f"Tempo: {registro.tempo} Dias")
        print(f"Diária: R${registro.diaria}")
        print(f"Valor Total: R${registro.valor_total}")
        print(f'ocupado: {registro.ocupado}')
        print(f'{96 * "_"}')


    def ler_registro(self, arquivo):

        try:
            registro_bytes = arquivo.read(self.tamanho_registro())

            if len(registro_bytes) < self.tamanho_registro():
                return None  # Evita leitura incompleta

            # Desempacota os dados
            ocupado, proximo, codigo, id_cliente, nome_cliente, id_carro, id_filial, data_aluguel, tempo, diaria, valor_total = \
                struct.unpack(self.get_formato(), registro_bytes)
            return Aluguel(
                ocupado=ocupado,
                proximo=proximo,
                codigo=codigo,
                cliente=Cliente(codigo=id_cliente, nome=nome_cliente.decode('utf-8').rstrip(chr(0))),
                carro=Carro(codigo=id_carro),
                filial=Filial(codigo=id_filial),
                data_aluguel=data_aluguel.decode('utf-8').rstrip(chr(0)),
                diaria=diaria,
                tempo=tempo,
                valor_total=valor_total,
            )

        except struct.error as e:
            print(f"Erro ao desempacotar registro: {e}")
        except UnicodeDecodeError as e:
            print(f"Erro ao decodificar: {e}")

    def criar_base(self, tamanho, desordenada=True,tabela_hash=None, **kwargs):


        arquivo = kwargs.get('arquivo')
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        if c_carros.quantidade_registros(arquivo_carro) < tamanho:
            raise ValueError("Não há carros suficientes para alugar")
        if arquivo is None:
            raise ValueError("O arquivo não foi informado")

        print(f'Gerando a base de dados tamanho {tamanho}...')
        codigos = [49, 51, 59, 3, 87, 103,  # seus elementos originais
             12, 34, 56, 78, 90, 123, 45, 67, 89, 101,
             23, 46, 68, 91, 114, 137, 159, 182, 205,
             28, 52, 77, 102, 127, 153, 179, 206, 233,
             31, 63, 96, 130, 165, 201, 238, 276, 315,
             37, 75, 114, 154, 195, 237, 280, 324]

        #
        # for i in range(tamanho):
        #     codigos.append(random.randint(1, 1000))
        for i in range(len(codigos)):
            arquivo.seek(i*self.tamanho_registro())
            print('Gerando registro endereco', arquivo.tell())
            registro = self.criar_registro(codigo=codigos[i], arquivo_cliente=arquivo_cliente,
                                           arquivo_carro=arquivo_carro,
                                           arquivo_filial=arquivo_filial)
            tabela_hash.insercao(registro)

    def get_formato(self):
        return '=?iii30sii10siii'

    def tamanho_registro(self):
        return int(struct.calcsize(self.get_formato()))

    @staticmethod
    def escolher_registro_aleatorio(arquivo, entidade):
        tamanho = entidade.tamanho_arquivo(arquivo)
        quant_arquivos = tamanho // entidade.tamanho_registro()
        posicao = random.randint(0, quant_arquivos - 1)
        arquivo.seek(posicao * entidade.tamanho_registro())
        registro_lido = entidade.ler_registro(arquivo)
        return registro_lido



