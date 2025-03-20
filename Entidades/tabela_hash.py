import struct

from Entidades.aluguel import Aluguel


class TabelaHashDisco:
    def __init__(self, m, arquivo_tabela, arquivo_lista):
        self.m = m  # Tamanho da tabela
        self.arquivo_tabela = arquivo_tabela  # Arquivo para armazenar a tabela hash
        self.arquivo_lista = arquivo_lista  # Arquivo para armazenar as listas encadeadas
        self.aluguel = Aluguel()

        # Inicializa a tabela com None (indicando que todos os compartimentos estão vazios)
        arquivo_tabela.write(struct.pack('I', 0) * m)

        # Inic ializa os ponteiros para as listas encadeadas
        arquivo_lista.write(struct.pack('I', -1) * m)  # -1 para indicar que a lista está vazia

    def hash_function(self, chave):
        """
        Função de hash simples utilizando o operador módulo.
        """
        return chave % self.m

    def buscar(self, chave):
        h = self.hash_function(chave)
        self.arquivo_tabela.seek(h * 4)
        rrn = struct.unpack('I', self.arquivo_tabela.read(4))[0]
        if rrn == -1:
            return None
        while True:
            self.arquivo_lista.seek(rrn * 4)
            aluguel_proximo = self.aluguel.ler_registro(self.arquivo_lista)

            if aluguel_proximo.codigo == chave:
                return rrn
            if aluguel_proximo.proximo == -1:
                return None
            rrn = aluguel_proximo.proximo

    def inserir(self, registro):
        self.buscar(registro.codigo)


