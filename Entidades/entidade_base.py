import struct
from faker import Faker
from random import shuffle

fake = Faker('pt_BR')


class EntidadeBase:
    def __init__(self):
        self.fake = fake

    def criar_registro(self, cod, **kwargs):
        """
        Subclasses devem implementar este método para retornar os atributos específicos do registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método criar_registro")

    def salvar_registro(self, arquivo=None, registro=None):
        formato = self.get_formato()
        dados_binarios = struct.pack(formato, *registro)

        arquivo.write(dados_binarios)

    @classmethod
    def ler_registro(cls, arquivo):
        try:
            formato = cls.get_formato()
            tamanho_registro = struct.calcsize(formato)
            registro_bytes = arquivo.read(tamanho_registro)
            if len(registro_bytes) < tamanho_registro:
                return None

            return struct.unpack(formato, registro_bytes)

        except struct.error as e:
            print(f"Erro ao desempacotar registro: {e}")
            return None

    def imprimir_registro(self, arquivo):
        """
        Subclasses devem implementar este método para imprimir o registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método imprimir_registro")

    def criar_base(self, tamanho, **kwargs):
        arquivo = kwargs.get('arquivo')
        if arquivo is None:
            raise ValueError("O arquivo não foi informado")

        print(f'Gerando {tamanho} registros...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        shuffle(codigos)
        for i in codigos:
            registro_criado = (self.criar_registro(i, arquivo=arquivo))
            self.salvar_registro(arquivo=arquivo, registro=registro_criado)

    def imprimir_base(self, arquivo):
        arquivo.seek(0)

        while registro_lido := self.ler_registro(arquivo):
                if registro_lido[0] is None:
                    print('erro1')
                    break

                self.imprimir_registro(registro_lido)


    @classmethod
    def get_formato(cls):
        print('=' * 80)
        """
        Subclasses devem implementar este método para retornar o formato do struct.
        """
        raise NotImplementedError("Subclasses devem implementar o método get_formato")
