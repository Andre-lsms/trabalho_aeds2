from Entidades.aluguel import Aluguel
class tabela_hash:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        # Inicializa a tabela com None
        self.tabela = [None] * tamanho

    def hash(self, cod):
        return cod % self.tamanho

    def buscar(self,cod):
        h = self.hash(cod)
        p = self.tabela[h]
        while p and p.codigo != cod:
            p = p.proximo
        return p

    def inserir(self, registro):
        h = self.hash(registro.codigo)
        p = self.tabela[h]
        anterior = None
        while p and p.codigo != registro.codigo:
            anterior = p
            p = p.proximo
        if p:
            p = registro
        else:
            novo = Aluguel()