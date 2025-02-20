import struct
import time
from random import shuffle

from faker import Faker

fake = Faker('pt_BR')


class EntidadeBase:
    def __init__(self, ):
        self.fake = fake
        self.topo = -1

    def criar_registro(self, codigo, **kwargs):
        raise NotImplementedError("Subclasses devem implementar o método criar_registro")

    def salvar_registro(self, arquivo, registro):
        raise NotImplementedError("Subclasses devem implementar o método criar_registro")

    def ler_registro(self, arquivo):
        """
        Subclasses devem implementar este método para ler um registro do arquivo.
        """
        raise NotImplementedError("Subclasses devem implementar o método ler_registro")

    def imprimir(self, registro,):
        """
        Subclasses devem implementar este método para imprimir o registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método imprimir_registro")

    def criar_base(self, tamanho, desordenada=True, **kwargs):
        arquivo = kwargs.get('arquivo')

        if arquivo is None:
            raise ValueError("O arquivo não foi informado")

        print(f'Gerando a base de daso tamanho {tamanho}...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        if desordenada:
            shuffle(codigos)
        for i in range(len(codigos)):
            registro = self.criar_registro(codigos[i], arquivo=arquivo)
            self.salvar_registro(arquivo, registro)

    def imprimir_base(self, arquivo):
        arquivo.seek(4)
        while registro_lido := self.ler_registro(arquivo):
            if registro_lido is not None:
                self.imprimir(registro_lido)

    def tamanho_registro(self):
        raise NotImplementedError("Subclasses devem implementar o método tamanho_registro")

    @staticmethod
    def tamanho_arquivo(arquivo):
        arquivo.seek(0, 2)
        tamanho = arquivo.tell()
        return int(tamanho-4)

    def quantidade_registros(self, arquivo):
        return self.tamanho_arquivo(arquivo) // self.tamanho_registro()

    def get_formato(self):
        """
        Subclasses devem implementar este método para retornar o formato do registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método get_formato")

    def sobrescrever(self, arquivo, registro):
        posicao = arquivo.tell()
        tamanho_registro = registro.tamanho_registro()
        arquivo.seek(posicao - tamanho_registro)
        registro.salvar_registro(arquivo, registro)

    def desordenar_base(self, arquivo):
        # Lê todos os registros do arquivo e armazena em uma lista
        registros = []
        arquivo.seek(4)  # Volta para o início do arquivo
        while registro_lido := self.ler_registro(arquivo):
            if registro_lido is not None and registro_lido != -1:
                registros.append(registro_lido)

        # Desordena a lista de registros
        shuffle(registros)

        # Reescreve os registros desordenados no arquivo
        arquivo.seek(0)  # Volta para o início do arquivo
        arquivo.truncate()
        arquivo.write(struct.pack('i', -1))
        for registro in registros:
            self.salvar_registro(arquivo, registro)

        print("Base desordenada com sucesso!")

    def ordenar_base(self, arquivo):
        t_inicio = time.time()
        registros = []

        # Lê todos os registros corretamente
        arquivo.seek(4)
        while registro_lido := self.ler_registro(arquivo):
            if registro_lido is not None and registro_lido != -1:
                registros.append(registro_lido)
        # Ordena corretamente pela chave 'codigo'
        registros.sort(key=lambda x: x.codigo)

        # Volta ao início do arquivo e reescreve os registros ordenados
        arquivo.seek(0)
        arquivo.truncate()
        arquivo.write(struct.pack('i', -1))
        # Apaga o conteúdo antigo

        for registro in registros:
            self.salvar_registro(arquivo, registro)  # Salva corretamente cada registro

        print(f"Base ordenada com sucesso! tempo de execução:{time.time() - t_inicio} ")

    # def ordenar_base(self, arquivo):
    #     # Lê todos os registros do arquivo e armazena em uma lista
    #     for j in range(1, self.quantidade_registros(arquivo)):
    #         arquivo.seek(j * self.tamanho_registro())
    #         registroj = self.ler_registro(arquivo)
    #         i = j - 1
    #         arquivo.seek(i * self.tamanho_registro())
    #         registroi = self.ler_registro(arquivo)
    #         while i >= 0 and registroi.codigo > registroj.codigo:
    #             arquivo.seek((i + 1) * self.tamanho_registro())
    #             self.salvar_registro(arquivo, registroi)
    #             i = i - 1
    #             if i >= 0:
    #                 arquivo.seek(i * self.tamanho_registro())
    #                 registroi = self.ler_registro(arquivo)
    #         arquivo.seek((i + 1) * self.tamanho_registro())
    #         self.salvar_registro(arquivo, registroj)
    #     print("Base ordenada com sucesso!")

