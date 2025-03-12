import os
import shutil
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

    def imprimir(self, registro, ):
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
        return int(tamanho - 4)

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

    import os
    import shutil

    import os
    import shutil
    import struct

    def selecao_natural(self, arquivo, m):
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

        # Posiciona no início do arquivo (depois do cabeçalho)
        arquivo.seek(4)
        reservatorio.seek(4)

        registros = []
        particao_atual = 0
        arquivo_saida = open(f'{caminho}/particao_{particao_atual}.dat', 'w+b')
        arquivo_saida.write(struct.pack('i', -1))

        # Cria o arquivo para o reservatório (no disco)

        # 1. Ler M registros do arquivo para a memória
        for i in range(m):
            registro = self.ler_registro(arquivo)
            if registro:
                registros.append(registro)
        # print(f'\033[94m[Inicialização]\033[0m Memória = {[r.codigo for r in registros]}')

        ultimo_gravado = None  # Último registro gravado na partição atual
        while True:
            # 2. Selecionar, no array em memória, o registro r com menor chave
            if registros:
                menor = min(registros, key=lambda x: x.codigo)

                # 3. Gravar o registro r na partição de saída
                self.salvar_registro(arquivo_saida, menor)
                ultimo_gravado = menor.codigo
                registros.remove(menor)
                # print(f'\033[92m[GRAVADO]\033[0m {menor.codigo} na partição {particao_atual}')

                # 4. Substituir, no array em memória, o registro r pelo próximo registro do arquivo de entrada
                novo_registro = self.ler_registro(arquivo)
                # print(f'\033[93m[Próximo Registro]\033[0m {novo_registro.codigo if novo_registro else None}')
                if novo_registro is not None:
                    if novo_registro.codigo < ultimo_gravado:
                        self.salvar_registro(reservatorio, novo_registro)
                        # print(f'\033[91m[MOVIDO PARA RESERVATÓRIO]\033[0m {novo_registro.codigo}')
                        # print(f'Estado do resevatório:')
                        # self.imprimir_codigos(reservatorio)
                    else:
                        registros.append(novo_registro)
            else:
                # print(
                #     f'\033[96m[Estado Atual]\033[0m Memória = {[r.codigo for r in registros]} | Reservatório = {self.quantidade_registros(reservatorio)} | Último Gravado = {ultimo_gravado}')
                if not registros and self.quantidade_registros(reservatorio) == 0:
                    break
                if self.quantidade_registros(reservatorio) == m or not registros:
                    # print(f'\033[95m[PARTIÇÃO FECHADA]\033[0m Criando partição {particao_atual + 1}')

                    for i in range(m):
                        if registros:
                            menor_atual = min(registros, key=lambda x: x.codigo)
                            self.salvar_registro(arquivo_saida, menor_atual)
                            print(f'\033[92m[GRAVADO]\033[0m {menor_atual.codigo} na partição {particao_atual}')
                            registros.remove(menor_atual)

                    arquivo_saida.close()
                    particao_atual += 1
                    arquivo_saida = open(f'{caminho}/particao_{particao_atual}.dat', 'w+b')
                    arquivo_saida.write(struct.pack('i', -1))

                reservatorio.seek(4)
                for i in range(m):
                    reg_reservatorio = self.ler_registro(reservatorio)
                    # print(f'\033[91m[Reservatório]\033[0m {reg_reservatorio.codigo if reg_reservatorio else None}')
                    if reg_reservatorio:
                        registros.append(reg_reservatorio)
                    else:
                        break

                    # Limpa o reservatório
                reservatorio.seek(4)
                # print(f'\033[94m[LIMPAR RESERVATÓRIO]\033[0m')
                reservatorio.truncate()
                ultimo_gravado = None

                if not registros:
                    break
        reservatorio.close()
        if os.path.exists(reservatorio_path):
            os.remove(reservatorio_path)
        # print(
        #     f'\033[94m[FIM]\033[0m Reservatório = {self.quantidade_registros(reservatorio)}, Memória = {len(registros)}')

    def intercalacao_otima(self, f):
        caminho = f'Bases/Particoes/{self.__class__.__name__}'

        arquivos = [arquivo for arquivo in os.listdir(caminho) if
                    arquivo.startswith('particao_') and arquivo.endswith('.dat')]

        qnt_arquivos = len(arquivos)
        num_part = qnt_arquivos
        while qnt_arquivos > 1:
            particoes = []
            for i in range(min(f - 1, qnt_arquivos)):
                if i < len(arquivos):
                    particoes.append(open(f'{caminho}/{arquivos[i]}', 'r+b'))
            saida = open(f'{caminho}/particao_{num_part}.dat', 'w+b')
            saida.write(struct.pack('i', -1))
            self.intercalacao_basica(particoes, saida)
            saida.close()
            num_part += 1
            qnt_arquivos = len(arquivos)

            arquivos = arquivos[min(f - 1, qnt_arquivos):] + [f'particao_{num_part - 1}.dat']
        if qnt_arquivos == 1:

            origem = f'{caminho}/{arquivos[0]}'  # Caminho do arquivo original
            destino = f'Bases/{self.__class__.__name__}.dat'  # Novo caminho e nome
            # Criar a pasta de destino se não existir
            os.makedirs(os.path.dirname(destino), exist_ok=True)

            # Mover e renomear o arquivo
            shutil.move(origem, destino)



        # while qnt_arquivos !=1:



    def intercalacao_basica(self, particoes, saida):
        num_p = len(particoes)
        saida.seek(4)
        fim = 0
        arquivos = []
        for i in range(num_p):
            arquivo = particoes[i]
            arquivo.seek(4)
            registro = self.ler_registro(arquivo)
            if registro:
                arquivos.append((arquivo, registro))
            else:
                arquivo.close()
                print(f'Arquivo {arquivos} vazio')
                print(f'registro {registro}')
                arquivos.append((None,None))
                os.remove(arquivo.name)

        while not fim:
            menor = None
            pos_menor = None
            for i in range(num_p):
                # print(f'menor {arquivos[i][1].codigo}')
                if arquivos[i] is not None and arquivos[i][1] is not None:
                    if menor is None or arquivos[i][1].codigo < menor.codigo:
                        menor = arquivos[i][1]
                        pos_menor = i
            if menor is None:
                fim = 1
            else:
                self.salvar_registro(saida, menor)
                novo_registro = self.ler_registro(arquivos[pos_menor][0])
                if novo_registro:
                    arquivos[pos_menor] = (arquivos[pos_menor][0], novo_registro)
                else:
                    arquivos[pos_menor][0].close()
                    os.remove(arquivos[pos_menor][0].name)
                    arquivos[pos_menor] = (None, None)

        for i in range(num_p):
            if arquivos[i] and arquivos[i][0]:
                arquivos[i][0].close()

    def imprimir_codigos(self, arquivo):
        arquivo.seek(4)  # Pular os primeiros 4 bytes, como no seu código original
        codigos = []

        # Lê os registros e coleta os códigos
        while registro_lido := self.ler_registro(arquivo):
            if registro_lido is not None:
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

    def ordenar_base(self, arquivo, m):
        self.selecao_natural(arquivo, m)
        self.intercalacao_otima(m)
        print(f'Base {self.__class__.__name__} ordenada com sucesso!')
