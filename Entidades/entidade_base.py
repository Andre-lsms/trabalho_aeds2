import os
import shutil
import struct
import time
from random import shuffle
from symtable import Class

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

    def imprimir(self, registro, ):
        """
        Subclasses devem implementar este método para imprimir o registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método imprimir_registro")

    def criar_base(self, tamanho, desordenada=True, **kwargs):
        arquivo = kwargs.get('arquivo')

        if arquivo is None:
            raise ValueError("O arquivo não foi informado")

        print(f'Gerando a base de dados tamanho {tamanho}...')
        codigos = []
        for i in range(tamanho):
            codigos.append(i + 1)
        if desordenada:
            shuffle(codigos)
        for i in range(len(codigos)):
            registro = self.criar_registro(codigos[i], arquivo=arquivo)
            self.salvar_registro(arquivo, registro)

    def imprimir_base(self, arquivo):
        arquivo.seek(0)
        while registro_lido := self.ler_registro(arquivo):
            if registro_lido is not None:
                self.imprimir(registro_lido)

    def tamanho_registro(self):
        raise NotImplementedError("Subclasses devem implementar o método tamanho_registro")

    @staticmethod
    def tamanho_arquivo(arquivo):
        arquivo.seek(0, 2)
        tamanho = arquivo.tell()
        return int(tamanho)

    def quantidade_registros(self, arquivo):
        return self.tamanho_arquivo(arquivo) // self.tamanho_registro()

    def get_formato(self):
        """
        Subclasses devem implementar este método para retornar o formato do registro.
        """
        raise NotImplementedError("Subclasses devem implementar o método get_formato")

    def selecao_natural(self, arquivo, m, depuracao=False):
        global novo_registro
        leituras = 0
        escritas = 0
        t_ini = time.time()
        caminho = f'Bases/Particoes/{self.__class__.__name__}'

        # Se existir, remove e recria o diretório
        if os.path.exists(caminho):
            shutil.rmtree(caminho)
        os.makedirs(caminho)
        reservatorio_path = f'{caminho}/reservatorio.dat'
        if os.path.exists(reservatorio_path):
            os.remove(reservatorio_path)
        reservatorio = open(reservatorio_path, 'w+b')
        reservatorio.write(struct.pack('i', -5))

        # Posiciona no início do arquivo
        arquivo.seek(0)
        reservatorio.seek(0)

        registros = []
        particao_atual = 0

        arquivo_saida = open(f'{caminho}/particao_{particao_atual}.dat', 'w+b')
        arquivo_saida.write(struct.pack('i', -1))

        # 1. Ler M registros do arquivo para a memória
        for i in range(m):
            registro = self.ler_registro(arquivo)
            leituras += 1
            if registro:
                registros.append(registro)

        if depuracao:
            print(
                f'\033[94m[INICIALIZANDO A MEMÓRIA]\033[0m | \033[94m[Memória]\033[0m = {[r.codigo for r in registros]}')

        # 2. Selecionar, no vetor em memória, o registro r com menor chave
        menor = min(registros, key=lambda x: x.codigo)
        # 3. Gravar o registro r na partição de saída
        self.salvar_registro(arquivo_saida, menor)
        escritas += 1
        ultimo_gravado = menor.codigo
        registros.remove(menor)

        if depuracao:
            quantidade_digitos = len(str(abs(menor.codigo)))
            espaco = ' ' * (10 - quantidade_digitos)
            print(f'\033[92m[GRAVADO]\033[0m {menor.codigo} na partição {particao_atual}{espaco}|', end='')

        while True:
            if registros:
                # 4. Substituir, no vetor em memória, o registro r pelo próximo do arquivo
                if ultimo_gravado != -1:
                    novo_registro = self.ler_registro(arquivo)
                    registros.append(novo_registro) if novo_registro else None
                    leituras += 1

                    if depuracao:
                        print(f' \033[94m[Memória]\033[0m = {[r.codigo for r in registros]}')
                # 5. Caso a chave do novo registro seja menor que a do último gravado, movê-lo para o reservatório
                if novo_registro:
                    if novo_registro.codigo < ultimo_gravado:
                        self.salvar_registro(reservatorio, novo_registro)
                        escritas += 1
                        registros.remove(novo_registro)
                        if depuracao:
                            quantidade_digitos = len(str(abs(novo_registro.codigo)))
                            espaco = ' ' * (7 - quantidade_digitos)
                            print(f'\033[36m[{novo_registro.codigo} MOVIDO PARA RESERVATÓRIO]\33[0m{espaco}|', end='')

                    else:
                        menor = min(registros, key=lambda x: x.codigo)
                        self.salvar_registro(arquivo_saida, menor)
                        escritas += 1
                        ultimo_gravado = menor.codigo
                        registros.remove(menor)
                        if depuracao:
                            quantidade_digitos = len(str(abs(menor.codigo)))
                            espaco = ' ' * (10 - quantidade_digitos)
                            print(f'\033[92m[GRAVADO]\033[0m {menor.codigo} na partição {particao_atual}{espaco}|',
                                  end='')
                else:
                    menor = min(registros, key=lambda x: x.codigo)
                    self.salvar_registro(arquivo_saida, menor)
                    escritas += 1
                    ultimo_gravado = menor.codigo
                    registros.remove(menor)
                    if depuracao:
                        quantidade_digitos = len(str(abs(menor.codigo)))
                        espaco = ' ' * (10 - quantidade_digitos)
                        print(f'\033[92m[GRAVADO]\033[0m {menor.codigo} na partição {particao_atual}{espaco}|', end='')

            if self.quantidade_registros(reservatorio) == m:
                if depuracao:
                    print(f' \033[31m[Reservatório cheio]\033[0m')
                    print(f'\033[94m[GRAVANDO ARQUIVO DO BUFFER]\033[0m{(6 * " ")}| \033[94m[Memória]\033[0m = {[r.codigo for r in registros]}')

                for i in range(m):
                    if registros:
                        menor_atual = min(registros, key=lambda x: x.codigo)
                        self.salvar_registro(arquivo_saida, menor_atual)
                        escritas += 1
                        registros.remove(menor_atual)
                        if depuracao:
                            quantidade_digitos = len(str(abs(menor_atual.codigo)))
                            espaco = ' ' * (10 - quantidade_digitos)
                            print(
                                f'\033[92m[GRAVADO]\033[0m {menor_atual.codigo} na partição {particao_atual}{espaco}|',
                                end='')
                            print(f' \033[94m[Memória]\033[0m = {[r.codigo for r in registros]}')
                    else:
                        break

                arquivo_saida.close()
                particao_atual += 1
                arquivo_saida = open(f'{caminho}/particao_{particao_atual}.dat', 'w+b')
                arquivo_saida.write(struct.pack('i', -1))

                reservatorio.seek(0)
                for i in range(m):
                    reg_reservatorio = self.ler_registro(reservatorio)
                    if reg_reservatorio:
                        registros.append(reg_reservatorio)
                    else:
                        break

                reservatorio.seek(0)
                reservatorio.truncate()
                ultimo_gravado = -1
                if depuracao:
                    print(f'\033[31m[CLONANDO RESERVATÓRIO]\033[0m {10* " "}| \033[94m[Memória]\033[0m = {[r.codigo for r in registros]}')

            if not registros:
                if self.quantidade_registros(reservatorio) > 0:
                    if depuracao:
                        print(f'\n\033[33m[ESVAZIANDO RESERVATÓRIO ANTES DE FINALIZAR]\033[0m')

                    reservatorio.seek(0)
                    while True:
                        reg_reservatorio = self.ler_registro(reservatorio)
                        if not reg_reservatorio:
                            break
                        registros.append(reg_reservatorio)

                    arquivo_saida.close()
                    particao_atual += 1
                    arquivo_saida = open(f'{caminho}/particao_{particao_atual}.dat', 'w+b')
                    arquivo_saida.write(struct.pack('i', -1))

                    while registros:
                        menor = min(registros, key=lambda x: x.codigo)
                        self.salvar_registro(arquivo_saida, menor)
                        registros.remove(menor)
                        if depuracao:
                            quantidade_digitos = len(str(abs(menor.codigo)))
                            espaco = ' ' * (10 - quantidade_digitos)
                            print(f'\033[92m[GRAVADO]\033[0m {menor.codigo} na partição {particao_atual}{espaco}|',
                                  end='')
                            print(f' \033[94m[Memória]\033[0m = {[r.codigo for r in registros]}')
                if depuracao:
                    print(f'\033[31m[REGISTROS ESGOTADOS]\033[0m')
                break

        reservatorio.close()
        if os.path.exists(reservatorio_path):
            os.remove(reservatorio_path)
        if depuracao:
            print(f'Quantidade de leituras: {leituras}')
            print(f'Quantidade de escritas: {escritas}')
            print(f'Tempo de execução: {time.time() - t_ini:.2f} segundos')
        return leituras, escritas, time.time() - t_ini
    def intercalacao_otima(self, f, depuracao=False):
        leituras = 0
        escritas = 0
        tempo_total = 0
        caminho = f'Bases/Particoes/{self.__class__.__name__}'
        arquivos = [arquivo for arquivo in os.listdir(caminho) if
                    arquivo.startswith('particao_') and arquivo.endswith('.dat')]
        qnt_arquivos = len(arquivos)
        num_part = qnt_arquivos

        if depuracao:
            print('\033[94m[INICIANDO INTERCALAÇÃO ÓTIMA]\033[0m')

        while qnt_arquivos != 1:
            particoes = []
            for i in range(min(f - 1, qnt_arquivos)):
                if i < len(arquivos):
                    particoes.append(open(f'{caminho}/{arquivos[i]}', 'r+b'))

            saida = open(f'{caminho}/particao_{num_part}.dat', 'w+b')
            saida.write(struct.pack('i', -1))

            if depuracao:
                print(f'\033[96m[INTERCALANDO {len(particoes)} partições]\033[0m {[p.name for p in particoes]} \033[0m  ')
            leituras_atuais, escritas_atuais,tempo_atuais  = self.intercalacao_basica(particoes, saida, depuracao)
            leituras += leituras_atuais
            escritas += escritas_atuais
            tempo_total += tempo_atuais

            for arquivo in particoes:
                arquivo.close()

            saida.close()
            num_part += 1

            arquivos = arquivos[min(f - 1, qnt_arquivos):] + [f'particao_{num_part - 1}.dat']
            qnt_arquivos = len(arquivos)

            if depuracao:
                print(f'\033[93m[NOVA PARTIÇÃO CRIADA]\033[0m particao_{num_part - 1}.dat')

        if qnt_arquivos == 1:
            origem = f'{caminho}/{arquivos[0]}'
            destino = f'Bases/{self.__class__.__name__}.dat'
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.move(origem, destino)

            if depuracao:
                print(f'\033[92m[INTERCALAÇÃO COMPLETA]\033[0m Arquivo final movido para {destino}')
                print(f'\033[94m[LEITURAS]\033[0m: {leituras}')
                print(f'\033[94m[ESCRITAS]\033[0m: {escritas}')
                print(f'\033[94m[TEMPO TOTAL]\033[0m: {tempo_total:.2f} segundos')
        return leituras, escritas,tempo_total

    def intercalacao_basica(self, particoes, saida, depuracao=False):
        num_p = len(particoes)
        saida.seek(0)
        fim = 0
        arquivos = []
        leituras = 0
        escritas = 0
        t_ini = time.time()

        if depuracao:
            print('\033[94m[INICIANDO INTERCALAÇÃO BÁSICA]\033[0m')

        # carrega o primeiro registro de cada arquivo
        for i in range(num_p):
            particoes[i].seek(0)
            registro = self.ler_registro(particoes[i])
            leituras += 1
            if registro:
                arquivos.append((particoes[i], registro))
                if depuracao:
                    print(f'\033[96m[CARREGADO]\033[0m Registro {registro.codigo} do arquivo {particoes[i].name}')
            else:
                particoes[i].close()
                if depuracao:
                    print(f'\033[91m[ARQUIVO VAZIO]\033[0m {particoes[i].name} removido')
                arquivos.append((None, None))
                os.remove(particoes[i].name)

        while not fim:
            menor = None
            pos_menor = None
            for i in range(num_p):
                if arquivos[i] is not None and arquivos[i][1] is not None:
                    if menor is None or arquivos[i][1].codigo < menor.codigo:
                        menor = arquivos[i][1]
                        pos_menor = i

            if menor is None:
                fim = 1
                if depuracao:
                    print('\033[91m[INTERCALAÇÃO FINALIZADA]\033[0m Nenhum registro restante')
            else:
                self.salvar_registro(saida, arquivos[pos_menor][1])
                escritas += 1
                if depuracao:
                    print(f'\033[92m[GRAVADO]\033[0m Registro {menor.codigo} na saída')

                novo_registro = self.ler_registro(arquivos[pos_menor][0])
                leituras += 1
                if novo_registro:
                    arquivos[pos_menor] = (arquivos[pos_menor][0], novo_registro)
                    if depuracao:
                        print(
                            f'\033[96m[NOVO REGISTRO]\033[0m {novo_registro.codigo} carregado de {arquivos[pos_menor][0].name}')
                else:
                    if depuracao:
                        print(f'\033[91m[ARQUIVO ENCERRADO]\033[0m {arquivos[pos_menor][0].name} removido')
                    arquivos[pos_menor][0].close()
                    os.remove(arquivos[pos_menor][0].name)
                    arquivos[pos_menor] = (None, None)

        for i in range(num_p):
            if arquivos[i] and arquivos[i][0]:
                arquivos[i][0].close()
                if depuracao:
                    print(f'\033[93m[FECHANDO ARQUIVO]\033[0m {arquivos[i][0].name}')

        return leituras, escritas , time.time() - t_ini

    def bubble_sort(self, arquivo, depuracao=False):
        quantidade = self.quantidade_registros(arquivo)
        leituras = 0
        escritas = 0
        t_ini = time.time()

        # Realiza a ordenação por Bubble Sort
        for i in range(quantidade - 1):
            trocou = False
            for j in range(quantidade - i - 1):
                # Lê os registros nas posições j e j+1
                arquivo.seek(4 + j * self.tamanho_registro())
                registro_atual = self.ler_registro(arquivo)
                leituras += 1

                arquivo.seek(4 + (j + 1) * self.tamanho_registro())
                registro_proximo = self.ler_registro(arquivo)
                leituras += 1

                # Depuração
                if depuracao:
                    print(
                        f"\033[94m[COMPARANDO]\033[0m Registro {registro_atual.codigo} com Registro {registro_proximo.codigo}")

                # Se o registro atual for maior que o próximo, realiza a troca
                if registro_atual.codigo > registro_proximo.codigo:
                    # Troca os registros diretamente no arquivo
                    self.trocar_registros(arquivo, j, j + 1, registro_atual, registro_proximo)
                    escritas += 2  # Contabilizando as escritas

                    # Depuração
                    if depuracao:
                        print(f"\033[92m[TROCANDO]\033[0m {registro_atual.codigo} com {registro_proximo.codigo}")

                    trocou = True

            # Se não houve troca, a lista já está ordenada
            if not trocou:
                break

        # Depuração de leituras e escritas ao final
        tempo_total = time.time() - t_ini
        if depuracao:
            print(f'\033[94m[LEITURAS]\033[0m: {leituras}')
            print(f'\033[94m[ESCRITAS]\033[0m: {escritas}')
            print(f'\033[94m[TEMPO TOTAL]\033[0m: {tempo_total:.2f} segundos')

        return leituras, escritas, tempo_total
    def trocar_registros(self, arquivo, posicao1, posicao2, registro1, registro2):
        """
        Troca os registros nas posições especificadas do arquivo.
        """
        # Escreve o registro1 na posição posicao2
        arquivo.seek(4 + posicao2 * self.tamanho_registro())
        self.salvar_registro(arquivo, registro1)

        # Escreve o registro2 na posição posicao1
        arquivo.seek(4 + posicao1 * self.tamanho_registro())
        self.salvar_registro(arquivo, registro2)

    def imprimir_codigos(self, arquivo):
        arquivo.seek(0)
        codigos = []

        # Lê os registros e coleta os códigos
        while registro_lido := self.ler_registro(arquivo):
            if registro_lido is not None and registro_lido.ocupado:
                codigos.append(registro_lido.codigo)

        # Exibe os códigos em formato de matriz
        if codigos:
            # Define a quantidade de códigos por linha
            colunas = 10
            linhas = [codigos[i:i + colunas] for i in range(0, len(codigos), colunas)]  # Cria as linhas de código

            # Imprime os códigos de forma organizada
            for linha in linhas:
                print("  ".join(f"{codigo:>6}" for codigo in linha))  # Formata cada número alinhado
        else:
            print("⚠️  Não há códigos para exibir!")

    def imprimir_todas_particoes(self):
        caminho = f'Bases/Particoes/{self.__class__.__name__}'
        arquivos = os.listdir(caminho)
        for nome_arquivo in arquivos:
            if nome_arquivo.startswith('particao_') and nome_arquivo.endswith('.dat'):
                caminho_arquivo = os.path.join(caminho, nome_arquivo)
                with open(caminho_arquivo, 'r+b') as arquivo:
                    quantidade = self.quantidade_registros(arquivo)

                    print(f'Conteúdo da {nome_arquivo}: [{quantidade} ]')
                    self.imprimir_codigos(arquivo)
                    print()  # Linha em branco para separar as partições

    def ordenar_base(self, arquivo, m,depuracao=False):
        self.selecao_natural(arquivo, m,depuracao = depuracao)
        self.intercalacao_otima(m,depuracao=depuracao)
        print(f'Base {self.__class__.__name__} ordenada com sucesso!')

    def sobrescrever(self, arquivo, registro):
        try:
            posicao = arquivo.tell()
            tamanho_registro = self.tamanho_registro()
            arquivo.seek(posicao - tamanho_registro)
            self.salvar_registro(arquivo, registro)
        except struct.error as e:
            print(f"Erro ao sobrescrever registro: {e}")