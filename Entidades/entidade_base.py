import struct
from faker import Faker
from random import shuffle

fake = Faker('pt_BR')


class EntidadeBase:
    def __init__(self, ):
        self.fake = fake

    def criar_registro(self, codigo, **kwargs):
        raise NotImplementedError("Subclasses devem implementar o método criar_registro")

    def salvar_registro(self, arquivo, registro):
        raise NotImplementedError("Subclasses devem implementar o método criar_registro")

        arquivo.seek(0, 2)

    def ler_registro(self, arquivo):
        """
        Subclasses devem implementar este método para ler um registro do arquivo.
        """
        raise NotImplementedError("Subclasses devem implementar o método ler_registro")

    def imprimir(self, registro):
        """
        Subclasses devem implementar este método para imprimir o registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método imprimir_registro")

    def criar_base(self, tamanho, **kwargs):
        arquivo = kwargs.get('arquivo')
        if arquivo is None:
            raise ValueError("O arquivo não foi informado")

        print(f'Gerando a base de daso tamanho {tamanho}...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        # shuffle(codigos)
        for i in range(len(codigos)):
            registro = self.criar_registro(codigos[i])
            self.salvar_registro(arquivo, registro)

    def imprimir_base(self, arquivo):
        arquivo.seek(0)
        while registro_lido := self.ler_registro(arquivo):
            if registro_lido is not None:
                self.imprimir(registro_lido)

    def tamanho_registro(self):
        raise NotImplementedError("Subclasses devem implementar o método tamanho_registro")

    def tamanho_arquivo(self, arquivo):
        arquivo.seek(0,2)
        tamanho = arquivo.tell()
        return int(tamanho)

    def get_formato(self):
        """
        Subclasses devem implementar este método para retornar o formato do registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método get_formato")
