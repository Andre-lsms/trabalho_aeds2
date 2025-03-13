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

    def __init__(self, marcador=None, rnn_proximo=0, codigo=0, cliente: Cliente = None, carro: Carro = None,
                 filial: Filial = None,
                 diaria=0,
                 data_aluguel=None, tempo=0, valor_total=0, ):
        super().__init__()
        self.nome_classe = 'Aluguel'
        self.marcador = marcador
        self.rnn_proximo = rnn_proximo
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
        arquivo.write(struct.pack('2s', registro.marcador.encode('utf-8')))
        arquivo.write(struct.pack('i', registro.rnn_proximo))
        arquivo.write(struct.pack('i', registro.codigo))
        arquivo.write(struct.pack('i', registro.cliente.codigo))
        arquivo.write(struct.pack('30s', registro.cliente.nome.encode('utf-8')))
        arquivo.write(struct.pack('i', registro.carro.codigo))
        arquivo.write(struct.pack('i', registro.filial.codigo))
        arquivo.write(struct.pack('10s', registro.data_aluguel.encode('utf-8')))
        arquivo.write(struct.pack('i', registro.tempo))
        arquivo.write(struct.pack('i', registro.diaria))
        arquivo.write(struct.pack('i', registro.valor_total))

    def excluir_registro(self, arquivo, registro):
        rrn = arquivo.tell() - self.tamanho_registro()
        topo_pilha = self.ler_topo_pilha(arquivo)
        arquivo.seek(rrn)
        registro.marcador = '*|'
        registro.rnn_proximo = topo_pilha
        arquivo.write(struct.pack('2s', registro.marcador.encode('utf-8')))
        arquivo.write(struct.pack('i', registro.rnn_proximo))
        arquivo.write(struct.pack('i', 0))
        arquivo.write(struct.pack('i', 0))
        arquivo.write(struct.pack('30s', registro.cliente.nome.encode('utf-8')))
        arquivo.write(struct.pack('i', 0))
        arquivo.write(struct.pack('i', 0))
        arquivo.write(struct.pack('10s', registro.data_aluguel.encode('utf-8')))
        arquivo.write(struct.pack('i', 0))
        arquivo.write(struct.pack('i', 0))
        arquivo.write(struct.pack('i', registro.valor_total))
        #  Atualiza o topo da pilha
        self.escrever_topo_pilha(arquivo, rrn)

    def adicionar_registro(self, arquivo, registro):
        rrn_disponivel = self.remover_da_pilha(arquivo)
        if rrn_disponivel is not None:
            arquivo.seek(rrn_disponivel)  # Posiciona no espaço disponível
        else:
            arquivo.seek(0, 2)  # Adiciona no final caso não haja espaço disponível
        self.salvar_registro(arquivo, registro)

    def remover_da_pilha(self, arquivo):
        #  Lê o topo da pilha
        topo_pilha = self.ler_topo_pilha(arquivo)

        if topo_pilha == -1:
            return None

        arquivo.seek(topo_pilha)
        registro = self.ler_registro(arquivo)
        proximo_topo = registro.rnn_proximo
        self.escrever_topo_pilha(arquivo, proximo_topo)
        return topo_pilha

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
            marcador='|',
            rnn_proximo=-1,
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
        if registro.marcador == '*|':
            return
        else:
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
            print(f'{96 * "_"}')

    def ler_registro(self, arquivo):
        try:
            posicao_atual = arquivo.tell()  # Salva posição inicial
            registro_bytes = arquivo.read(self.tamanho_registro())

            if len(registro_bytes) < self.tamanho_registro():
                return None  # Evita leitura incompleta

            # Desempacota os dados
            marcador, rnn_proximo, codigo, id_cliente, nome_cliente, id_carro, id_filial, data_aluguel, tempo, diaria, valor_total = \
                struct.unpack(self.get_formato(), registro_bytes)

            # Se for um registro excluído (*|), ignorar
            if marcador == '*|':
                return -1
            return Aluguel(
                marcador=marcador.decode('utf-8').rstrip(chr(0)),
                rnn_proximo=rnn_proximo,
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
            print(f"Erro ao desempacotar registro na posição {posicao_atual}: {e}")
        except UnicodeDecodeError as e:
            print(f"Erro ao decodificar marcador na posição {posicao_atual}: {e}")

    def criar_base(self, tamanho, desordenada=True, **kwargs):
        arquivo = kwargs.get('arquivo')
        arquivo_cliente = kwargs.get('arquivo_cliente')
        arquivo_carro = kwargs.get('arquivo_carro')
        arquivo_filial = kwargs.get('arquivo_filial')
        if c_carros.quantidade_registros(arquivo_carro) < tamanho:
            raise ValueError("Não há carros suficientes para alugar")
        if arquivo is None:
            raise ValueError("O arquivo não foi informado")

        print(f'Gerando a base de dados tamanho {tamanho}...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        if desordenada:
            random.shuffle(codigos)
        for i in range(len(codigos)):
            registro = self.criar_registro(codigo=codigos[i], arquivo_cliente=arquivo_cliente,
                                           arquivo_carro=arquivo_carro,
                                           arquivo_filial=arquivo_filial)
            self.salvar_registro(arquivo, registro)

    def get_formato(self):
        return '=2siii30sii10siii'

    def tamanho_registro(self):
        return int(struct.calcsize(self.get_formato()))

    @staticmethod
    def escolher_registro_aleatorio(arquivo, entidade):
        tamanho = entidade.tamanho_arquivo(arquivo)
        quant_arquivos = tamanho // entidade.tamanho_registro()
        posicao = random.randint(0, quant_arquivos - 1)
        arquivo.seek(posicao * entidade.tamanho_registro() + 4)
        registro_lido = entidade.ler_registro(arquivo)
        return registro_lido

