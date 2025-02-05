import struct
from Entidades.entidade_base import EntidadeBase
from Funcoes.geradores import gerar_telefone_aleatorio, gerar_endereco


class Filial(EntidadeBase):
    def __init__(self, codigo=0, nome=None, endereco=None, telefone=None, email=None):
        super().__init__()
        self.nome_classe = 'Filial'
        self.codigo = codigo
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    def criar_registro(self, codigo, **kwargs):
        self.codigo = codigo
        self.nome = kwargs.get('nome'[:30], (self.fake.company())[:30])
        self.email = kwargs.get('email'[:30], self.fake.email()[:30])
        self.telefone = kwargs.get('telefone'[:15], gerar_telefone_aleatorio())
        self.endereco = kwargs.get('endereco'[:70], gerar_endereco()[:70])
        return Filial(
            codigo=codigo,
            nome=self.nome,
            email=self.email,
            telefone=self.telefone,
            endereco=self.endereco
        )
    def salvar_registro(self, arquivo, registro):
        try:
            arquivo.write(struct.pack('i', registro.codigo))
            arquivo.write(struct.pack('30s', registro.nome.encode('utf-8')))
            arquivo.write(struct.pack('30s', registro.email.encode('utf-8')))
            arquivo.write(struct.pack('15s', registro.telefone.encode('utf-8')))
            arquivo.write(struct.pack('70s', registro.endereco.encode('utf-8')))
        except struct.error as e:
            print(f"Erro ao empacotar registro: {e}")
    def imprimir(self, registro):
        print(f'{95 * "_"}')
        print(f"Código: {registro.codigo}")
        print(f"Nome: {registro.nome.upper().strip()}")
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
            codigo, nome,email, telefone, endereco  = registro
            return Filial(
                codigo=codigo,
                nome=nome.decode('utf-8', errors='ignore').rstrip(chr(0)),
                email=email.decode('utf-8', errors='ignore').rstrip(chr(0)),
                telefone=telefone.decode('utf-8', errors='ignore').rstrip(chr(0)),
                endereco=endereco.decode('utf-8', errors='ignore').rstrip(chr(0)),  # Ignora bytes inválidos
            )
        except struct.error as e:
            print(f"Erro ao desempacotar registro: {e}")

    def get_formato(self):
        return '=i30s30s15s70s'

    def tamanho_registro(self):
        return struct.calcsize(self.get_formato())