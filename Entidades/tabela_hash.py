import struct
from Entidades.aluguel import Aluguel
from Entidades.carro import Carro

class Tabela_hash:
    def __init__(self, m, tabela, base):
        self.m = m
        self.tabela = tabela
        self.base = base
        self.aluguel = Aluguel()
        for i in range(m):
            self.tabela.write(struct.pack('i', -1))
        print("\33[34mTabela Hash Criada com sucesso!\33[0m")  # Mensagem inicial estilizada

    def hash(self, codigo):
        h = codigo % self.m
        print(f"\33[35mHash para {codigo}:\33[0m {h}")
        return h

    def busca(self, codigo):
        h = self.hash(codigo)
        self.tabela.seek(h * 4)
        endereco =  struct.unpack('i', self.tabela.read(4))[0]
        print('endereco: ', endereco)
        while True:
            self.base.seek(endereco)
            registro_atual = self.aluguel.ler_registro(self.base)
            if registro_atual.codigo == codigo and registro_atual.ocupado:
                print(f"\33[32mRegistro Encontrado\33[0m")
                self.aluguel.imprimir(registro_atual)
                return

            if registro_atual.proximo == -1:
                print(f"\33[31mFim da lista encadeada\33[0m ")
                break
            else:
                endereco = registro_atual.proximo
        print(f"\33[31mRegistro Não encontrado\33[0m")

    def insercao(self, registro):
        endereco = self.base.tell()
        h = self.hash(registro.codigo)
        self.tabela.seek(h * 4)
        endereco_atual = struct.unpack('i', self.tabela.read(4))[0]

        if endereco_atual == -1:
            self.tabela.seek(h * 4)
            self.tabela.write(struct.pack('i', endereco))
            self.base.seek(endereco)
            self.aluguel.salvar_registro(self.base, registro)
            print(f"\33[32mPrimeiro registro na posição:\33[0m {h} | \33[33mEndereço:\33[0m {endereco}")
            return

        while True:
            self.base.seek(endereco_atual)
            registro_atual = self.aluguel.ler_registro(self.base)

            if registro_atual.codigo == registro.codigo:
                if registro_atual.ocupado:
                    print(f"\33[32mRegistro já existe\33[0m")
                    return
                else:
                    self.base.seek(endereco_atual)
                    self.aluguel.salvar_registro(self.base, registro)
                    print(f"\33[33mInserindo na posição disponível\33[0m | Posição: {endereco_atual}")
                    return

            if registro_atual.proximo == -1:
                print('Registyro atual : ',registro_atual.codigo)
                registro_atual.proximo = endereco
                self.base.seek(endereco_atual)
                self.aluguel.salvar_registro(self.base, registro_atual)
                self.base.seek(endereco)
                self.aluguel.salvar_registro(self.base, registro)
                print(f"\33[33mInserindo no final da lista\33[0m")
                return

            endereco_atual = registro_atual.proximo

    def exclusao(self, codigo):
        h = self.hash(codigo)
        self.tabela.seek(h * 4)
        endereco_atual = struct.unpack('i', self.tabela.read(4))[0]

        if endereco_atual == -1:
            print(f"\33[31mRegistro não encontrado (lista vazia)\33[0m")
            return False

        anterior = None
        endereco_anterior = -1

        while endereco_atual != -1:
            self.base.seek(endereco_atual)
            registro_atual = self.aluguel.ler_registro(self.base)

            if registro_atual.codigo == codigo and registro_atual.ocupado:
                # Caso 1: É o primeiro da lista
                if anterior is None:
                    # Atualiza a tabela para apontar para o próximo
                    self.tabela.seek(h * 4)
                    self.tabela.write(struct.pack('i', registro_atual.proximo))
                else:
                    # Caso 2: Está no meio ou no final da lista
                    anterior.proximo = registro_atual.proximo
                    self.base.seek(endereco_anterior)
                    self.aluguel.salvar_registro(self.base, anterior)

                # Marca o registro como desocupado
                registro_atual.ocupado = False
                self.base.seek(endereco_atual)
                self.aluguel.salvar_registro(self.base, registro_atual)

                print(f"\33[32mRegistro {codigo} removido com sucesso\33[0m")
                return True

            endereco_anterior = endereco_atual
            anterior = registro_atual
            endereco_atual = registro_atual.proximo

        print(f"\33[31mRegistro {codigo} não encontrado\33[0m")
        return False
    def imprimir_tabela(self):
        print("\33[34m┏━━━━━━━━━━━━━ Tabela Hash ━━━━━━━━━━━━━┓\33[0m")  # Título estilizado
        for i in range(self.m):
            # Buscando o endereço armazenado no índice i
            self.tabela.seek(i * 4)
            endereco_atual = struct.unpack('i', self.tabela.read(4))[0]

            if endereco_atual != -1:
                # Exibindo o índice e o endereço
                print(f"\33[36mÍndice {i}: \33[33mEndereço {endereco_atual}\33[0m")

                # Percorrendo os registros encadeados
                while endereco_atual != -1:
                    self.base.seek(endereco_atual)
                    registro_atual = self.aluguel.ler_registro(self.base)

                    # Exibe as informações do registro
                    print(f"\33[32m  → Código:\33[0m \33[35m{registro_atual.codigo}\33[0m | "
                          f"\33[32mOcupado:\33[0m \33[33m{registro_atual.ocupado}\33[0m | "
                          f"\33[32mPróximo:\33[0m \33[36m{registro_atual.proximo}\33[0m")

                    endereco_atual = registro_atual.proximo
            else:
                # Caso o endereço seja -1 (não existe registro)
                print(f"\33[31mÍndice {i}: Nenhum registro (Valor -1)\33[0m")

        print("\33[34m┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\33[0m")  # Final estilizado
