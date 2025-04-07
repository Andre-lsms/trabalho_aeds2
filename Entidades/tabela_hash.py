import struct
from Entidades.aluguel import Aluguel
from Entidades.carro import Carro

class Tabela_hash:
    def __init__(self, m, tabela, base):
        self.m = m
        self.tabela = tabela
        self.base = base
        self.aluguel = Aluguel()


    def hash(self, codigo):
        h = codigo % self.m
        print(f"\n\33[36m[FUNÇÃO HASH]\33[0m")
        print(f"\33[35m• Hash calculado (codigo % m):\33[0m {h}")
        return h

    def busca(self, codigo):
        print(f"\n\33[36m[INICIANDO BUSCA]\33[0m \33[1mCódigo:\33[0m \33[35m{codigo}\33[0m")
        h = self.hash(codigo)

        self.tabela.seek(h * 4)
        endereco = struct.unpack('i', self.tabela.read(4))[0]
        print(f"\33[33m• Endereço inicial na tabela:\33[0m {endereco}")

        if endereco == -1:
            print("\33[31m• Lista vazia - Registro não encontrado!\33[0m")
            return

        while True:
            print(f"\33[33m• Acessando endereço na base:\33[0m {endereco}")
            self.base.seek(endereco)
            registro_atual = self.aluguel.ler_registro(self.base)

            print(f"\33[33m  → Código encontrado:\33[0m {registro_atual.codigo} | "
                  f"\33[33mOcupado:\33[0m {registro_atual.ocupado} | "
                  f"\33[33mPróximo:\33[0m {registro_atual.proximo}")

            if registro_atual.codigo == codigo and registro_atual.ocupado:
                print("\n\33[42m\33[1m• REGISTRO ENCONTRADO!\33[0m")
                self.aluguel.imprimir(registro_atual)
                return

            if registro_atual.proximo == -1:
                print("\33[41;1m• Fim da lista encadeada - Registro não encontrado!\33[0m")
                break

            endereco = registro_atual.proximo

    def insercao(self, registro):
        print(f"\n\33[36m[INICIANDO INSERÇÃO]\33[0m \33[1mCódigo:\33[0m \33[35m{registro.codigo}\33[0m")
        self.base.seek(0,2) # Endereço onde o novo registro seria inserido
        endereco_novo = self.base.tell()
        h = self.hash(registro.codigo)

        # Variáveis para rastrear a primeira posição disponível
        endereco_disponivel = None
        anterior_disponivel = None

        self.tabela.seek(h * 4)
        endereco_atual = struct.unpack('i', self.tabela.read(4))[0]
        print(f"\33[33m• Endereço inicial na tabela:\33[0m {endereco_atual}")

        # Caso 1: Lista vazia
        if endereco_atual == -1:
            print("\33[33m• Lista vazia - Inserindo como primeiro elemento\33[0m")
            self.tabela.seek(h * 4)
            self.tabela.write(struct.pack('i', endereco_novo))
            self.base.seek(endereco_novo)
            self.aluguel.salvar_registro(self.base, registro)
            print(f"\33[32m✓ Registro inserido com sucesso no endereço:\33[0m {endereco_novo}")
            return

        # Percorre a lista encadeada

        while True:
            print(f"\33[33m• Verificando endereço:\33[0m {endereco_atual}")
            self.base.seek(endereco_atual)
            registro_atual = self.aluguel.ler_registro(self.base)

            print(f"\33[33m  → Código encontrado:\33[0m {registro_atual.codigo} | "
                  f"\33[33mOcupado:\33[0m {registro_atual.ocupado} | "
                  f"\33[33mPróximo:\33[0m {registro_atual.proximo}")

            # Caso 2: Encontrou um registro desocupado (para reaproveitar)
            if not registro_atual.ocupado and endereco_disponivel is None:
                endereco_disponivel = endereco_atual
                anterior_disponivel = anterior
                print(f"\33[33m• Espaço disponível encontrado no endereço:\33[0m {endereco_disponivel}")

            # Caso 3: Registro já existe (ocupado)
            if registro_atual.codigo == registro.codigo and registro_atual.ocupado:
                print("\33[31m• Registro já existe e está ocupado!\33[0m")
                return

            # Fim da lista
            if registro_atual.proximo == -1:
                # Caso 4: Reaproveita espaço disponível se encontrado
                if endereco_disponivel is not None:
                    # Lê o registro desocupado para obter seu 'proximo' original
                    self.base.seek(endereco_disponivel)
                    registro_desocupado = self.aluguel.ler_registro(self.base)

                    # Mantém a cadeia original
                    registro.proximo = registro_desocupado.proximo  # ← Preserva o encadeamento!

                    # Sobrescreve o registro
                    self.base.seek(endereco_disponivel)
                    self.aluguel.salvar_registro(self.base, registro)

                    # Atualiza o ponteiro do anterior
                    if anterior_disponivel is None:
                        self.tabela.seek(h * 4)
                        self.tabela.write(struct.pack('i', endereco_disponivel))
                    else:
                        self.base.seek(anterior_disponivel)
                        reg_anterior = self.aluguel.ler_registro(self.base)
                        reg_anterior.proximo = endereco_disponivel
                        self.base.seek(anterior_disponivel)
                        self.aluguel.salvar_registro(self.base, reg_anterior)

                    print(f"\33[32m✓ Registro reaproveitado no endereço:\33[0m {endereco_disponivel}")
                    return
                else:
                    # Caso 5: Insere no final da lista
                    print("\33[33m• Fim da lista encontrado - Inserindo novo registro\33[0m")
                    registro_atual.proximo = endereco_novo
                    self.base.seek(endereco_atual)
                    self.aluguel.salvar_registro(self.base, registro_atual)
                    self.base.seek(endereco_novo)
                    registro.proximo = -1  # Novo registro é o último
                    self.aluguel.salvar_registro(self.base, registro)
                    print(f"\33[32m✓ Registro inserido no final. Endereço:\33[0m {endereco_novo}")
                    return

            anterior = endereco_atual
            endereco_atual = registro_atual.proximo
    def exclusao(self, codigo):
        print(f"\n\33[36m[INICIANDO EXCLUSÃO]\33[0m \33[1mCódigo:\33[0m \33[35m{codigo}\33[0m")
        h = self.hash(codigo)

        self.tabela.seek(h * 4)
        endereco_atual = struct.unpack('i', self.tabela.read(4))[0]
        print(f"\33[33m• Endereço inicial na tabela:\33[0m {endereco_atual}")

        if endereco_atual == -1:
            print("\33[31m• Lista vazia - Nada para excluir!\33[0m")
            return

        while endereco_atual != -1:
            print(f"\33[33m• Verificando endereço:\33[0m {endereco_atual}")
            self.base.seek(endereco_atual)
            registro_atual = self.aluguel.ler_registro(self.base)

            print(f"\33[33m  → Código encontrado:\33[0m {registro_atual.codigo} | "
                  f"\33[33mOcupado:\33[0m {registro_atual.ocupado} | "
                  f"\33[33mPróximo:\33[0m {registro_atual.proximo}")

            if registro_atual.codigo == codigo:
                if registro_atual.ocupado:
                    registro_atual.ocupado = False
                    self.base.seek(endereco_atual)
                    self.aluguel.salvar_registro(self.base, registro_atual)
                    print("\33[42m\33[1m✓ Registro excluído com sucesso!\33[0m")

                    return
                else:
                    print("\33[31m• Registro não existe!\33[0m")
                    return

            endereco_atual = registro_atual.proximo

        print("\33[41m\33[1m✗ Registro não encontrado para exclusão!\33[0m")
        return

    def imprimir_tabela(self):
        print("\n\33[1mTABELA HASH - RESUMO\33[0m")
        print("\33[90m" + "═" * 60 + "\33[0m")
        print("\33[1mÍndice  │ Endereço │ Código │ Ocupado │ Próximo\33[0m")

        for i in range(self.m):
            self.tabela.seek(i * 4)
            endereco_inicial = struct.unpack('i', self.tabela.read(4))[0]

            if i > 0:
                print("\33[90m" + "─" * 60 + "\33[0m")

            print(f"\33[36m{i:<7}\33[0m│", end=" ")

            if endereco_inicial == -1:
                print("\33[31m{empty:^8}│ {empty:^7}│ {empty:^8}│ {empty:^8}\33[0m".format(empty="-"))
                continue

            endereco_atual = endereco_inicial
            primeiro = True

            while endereco_atual != -1:
                self.base.seek(endereco_atual)
                registro = self.aluguel.ler_registro(self.base)

                if not primeiro:
                    print(f"\33[36m{' ':^7}\33[0m│", end=" ")

                print(f"{endereco_atual:<8}│ {registro.codigo:<7}│ {str(registro.ocupado):<8}│ {registro.proximo:<8}")

                endereco_atual = registro.proximo
                primeiro = False

        print("\33[90m" + "═" * 60 + "\33[0m\n")

    def inicializar_tabela(self):
        print("\n\33[36m[INICIALIZANDO TABELA]\33[0m")
        for i in range(self.m):
            self.tabela.seek(i * 4)
            self.tabela.write(struct.pack('i', -1))
        print("\33[32m✓ Tabela inicializada com sucesso!\33[0m")