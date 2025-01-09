import struct
from faker import Faker
from random import shuffle

fake = Faker('pt_BR')


class EntidadeBase:
    def __init__(self):
        self.fake = fake

    def criar_registro(self, cod, arquivo):
        """
        Subclasses devem implementar este método para retornar os atributos específicos do registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método criar_registro")

    def salvar_registro(self, cod, arquivo):
        registro = self.criar_registro(cod,arquivo)
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

    def imprimir_registro(self, registro):
        """
        Subclasses devem implementar este método para imprimir o registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método imprimir_registro")

    def criar_base(self, arquivo, tamanho):
        print(f'Gerando {tamanho} registros...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        shuffle(codigos)
        for i in codigos:
            self.salvar_registro(i, arquivo)

    def imprimir_base(self, arquivo):
        arquivo.seek(0)
        while True:
            try:
                self.imprimir_registro(arquivo)

            except Exception as e:
                break

    @classmethod
    def get_formato(cls):
        """
        Subclasses devem implementar este método para retornar o formato do struct.
        """
        raise NotImplementedError("Subclasses devem implementar o método get_formato")



