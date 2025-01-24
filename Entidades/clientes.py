import struct

from Entidades import funcoes
from Entidades.entidade_base import EntidadeBase


class Cliente(EntidadeBase):
    def __init__(self, cod=0, nome=None, idade=0, cpf=None, endereco=None, telefone=None, email=None):
        super().__init__()
        self.codigo = cod
        self.nome = nome
        self.idade = idade
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    def criar_registro(self, codigo, **kwargs):
        self.codigo = codigo
        self.nome = kwargs.get('nome'[:30], (self.fake.name())[:30])
        self.idade = kwargs.get('idade', self.fake.random_int(min=18, max=70))
        self.cpf = kwargs.get('cpf'[:14], self.fake.numerify(text='###.###.###-##')[:14])
        self.email = kwargs.get('email'[:30], self.fake.email()[:30])
        self.telefone = kwargs.get('telefone'[:20], self.fake.phone_number()[:20])
        self.endereco = kwargs.get('endereco'[:70], funcoes.gerar_endereco()[:70])
        return Cliente(
            cod=codigo,
            nome=self.nome,
            idade=self.idade,
            cpf=self.cpf,
            email=self.email,
            telefone=self.telefone,
            endereco=self.endereco
        )

    def salvar_registro(self, arquivo, registro):
        try:
            arquivo.write(struct.pack('i', registro.codigo))
            arquivo.write(struct.pack('30s', registro.nome.encode('utf-8')))
            arquivo.write(struct.pack('i', registro.idade))
            arquivo.write(struct.pack('14s', registro.cpf.encode('utf-8')))
            arquivo.write(struct.pack('30s', registro.email.encode('utf-8')))
            arquivo.write(struct.pack('20s', registro.telefone.encode('utf-8')))
            arquivo.write(struct.pack('70s', registro.endereco.encode('utf-8')))
        except struct.error as e:
            print(f"Erro ao empacotar registro: {e}")

    def imprimir(self, registro):
        print(f'{95 * "_"}')
        print(f"Código: {registro.codigo}")
        print(f"Nome: {registro.nome.strip()}")
        print(f"Idade: {registro.idade}")
        print(f"CPF: {registro.cpf.strip()}")
        print(f"Email: {registro.email.strip()}")
        print(f"Telefone: {registro.telefone.strip()}")
        print(f"Endereço: {registro.endereco.strip()}")
        print(f'{96 * "_"}')

    def ler_registro(self, arquivo):
        try:
            registro_bytes = arquivo.read(self.tamanho_registro())
            if len(registro_bytes) < self.tamanho_registro():
                return None

            registro = struct.unpack(self.get_formato(), registro_bytes)
            cod, nome, idade, cpf, email,telefone,endereco = registro

            # Cria uma nova instância de Cliente com os dados lidos
            return Cliente(
                cod=cod,
                nome=nome.decode('utf-8').rstrip(chr(0)),
                idade=idade,
                cpf=cpf.decode('utf-8').rstrip(chr(0)),
                email=email.decode('utf-8').rstrip(chr(0)),
                endereco=endereco.decode('utf-8').rstrip(chr(0)),
                telefone=telefone.decode('utf-8').rstrip(chr(0)),
            )
        except struct.error as e:
            print(f"Erro ao desempacotar registro: {e}")
            return None

    def get_formato(self):
        return "=i30si14s30s20s70s"

    def tamanho_registro(self):
        tamanho = struct.calcsize(self.get_formato())
        tamanho= int(tamanho)
        return tamanho
