import math
import struct
from random import randint
from time import time
from faker import Faker

fake = Faker('pt_BR')


def escolher_registro(arquivo, entidade, posicao=None):
    quantidade = (tamanho_arquivo(arquivo) // tamanho_registro(entidade))
    if posicao is None:
        posicao = fake.random_int(min=0, max=quantidade - 1)
    arquivo.seek((posicao * tamanho_registro(entidade)))
    registro_lido = entidade.ler_registro(arquivo)
    return registro_lido


def gerar_endereco():
    rua = fake.street_name()
    numero = fake.building_number()
    bairro = fake.bairro()
    cidade = fake.city()
    return rua + ', ' + numero + ' - ' + bairro + '. ' + cidade


def tamanho_arquivo(arquivo):
    arquivo.seek(0, 2)
    return arquivo.tell()


def tamanho_registro(entidade):
    return struct.calcsize(entidade.get_formato())


def quantidade_registros(arquivo, entidade):
    return tamanho_arquivo(arquivo) // tamanho_registro(entidade)


def pesquisa_sequencial(id, arquivo, endidade, arquivo_log):
    tipo_entidade=endidade.__class__.__name__
    tamanho = tamanho_arquivo(arquivo)
    tinicio = time()
    comparacoes = 0
    arquivo.seek(0)
    for i in range(tamanho // tamanho_registro(endidade)):
        registro = endidade.ler_registro(arquivo)
        comparacoes += 1
        if registro[0] == id:
            arquivo_log.write(95 * "_")
            arquivo_log.write('PESQUISA SEQUENCIAL id [{}] de [ {} ] '.format(id, tipo_entidade))
            arquivo_log.write(f'Foram realizadas {comparacoes} comparações\n')
            arquivo_log.write(f'A pesquisa sequencial levou {time() - tinicio} segundos\n')
            arquivo_log.write(95 * "_")
            return registro
    return -1


def pesquisa_binaria(id, arquivo, entidade, arquivo_log):
    tamanho = tamanho_arquivo(arquivo)
    total_registros = tamanho // tamanho_registro(entidade)
    tinicio = time()
    inicio = 0
    fim = total_registros - 1
    comparacoes = 0
    arquivo.seek(0)
    while inicio <= fim:
        meio = (inicio + fim) // 2
        arquivo.seek(meio * tamanho_registro(entidade))
        registro = entidade.ler_registro(arquivo)
        comparacoes += 1
        if registro[0] == id:
            arquivo_log.write(95 * "_")
            arquivo_log.write('PESQUISA BINÁRIA id [{}]\n'.format(id))
            arquivo_log.write(f'Foram realizadas {comparacoes} comparações\n')
            arquivo_log.write(f'A pesquisa binária levou {time() - tinicio} segundos\n')
            arquivo_log.write(95 * "_")
            return registro
        elif registro[0] < id:
            inicio = meio + 1
        elif registro[0] > id:
            fim = meio - 1
    return -1


def ler_ultimo_registro(arquivo, entidade):
    tamanho = tamanho_arquivo(arquivo)
    arquivo.seek(tamanho - tamanho_registro(entidade))
    registro: object = entidade.ler_registro(arquivo)
    return registro


def retornar_tamanho_tela():
    import tkinter as tk

    # Cria uma instância da janela
    root = tk.Tk()

    # Recupera o tamanho da tela
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Fecha a janela
    root.destroy()
    return screen_width, screen_height


def ler_log(arquivo_log, saida):
    arquivo_log.seek(0)
    log = arquivo_log.read()
    saida.write(log)



def desordenar_bases(arquivo, arquivo_log, entidade):
    tamanho = tamanho_arquivo(arquivo)
    total_registros = tamanho // tamanho_registro(entidade)

    for i in range(total_registros - 1, 0, -1):
        j = randint(0, i)

        # Read record i
        arquivo.seek(i * tamanho_registro(entidade))
        registro_i = entidade.ler_registro(arquivo)

        # Read record j
        arquivo.seek(j * tamanho_registro(entidade))
        registro_j = entidade.ler_registro(arquivo)

        # Swap record i and record j
        arquivo.seek(i * tamanho_registro(entidade))
        entidade.salvar_registro(arquivo, registro_j)

        arquivo.seek(j * tamanho_registro(entidade))
        entidade.salvar_registro(arquivo, registro_i)


def insertionsort(arquivo, arquivo_log, entidade):
    arquivo.seek(0)
    tamanho = tamanho_arquivo(arquivo)
    tinicio = time()
    comparacoes = 0

    for j in range(1, tamanho // tamanho_registro(entidade)):
        # Posiciona o ponteiro no registro j
        arquivo.seek(j * tamanho_registro(entidade))
        registro = entidade.ler_registro(arquivo)

        if registro is None:
            print(f"Erro: registro lido no índice {j} é None")
            break  # Saia para evitar mais erros

        i = j - 1

        # Posiciona o ponteiro no registro i
        arquivo.seek(i * tamanho_registro(entidade))
        registro_i = entidade.ler_registro(arquivo)

        comparacoes += 1

        while i >= 0 and registro_i[0] > registro[0]:
            # Posiciona o ponteiro no registro i+1
            arquivo.seek((i + 1) * tamanho_registro(entidade))
            entidade.salvar_registro(arquivo, registro_i)
            i -= 1

            if i >= 0:
                # Posiciona o ponteiro no registro i
                arquivo.seek(i * tamanho_registro(entidade))
                registro_i = entidade.ler_registro(arquivo)

            comparacoes += 1

        # Posiciona o ponteiro no registro i+1
        arquivo.seek((i + 1) * tamanho_registro(entidade))
        entidade.salvar_registro(arquivo, registro)

    arquivo_log.write(95 * "_")
    arquivo_log.write('INSERTION SORT\n')
    arquivo_log.write(f'Foram realizadas {comparacoes} comparações\n')
    arquivo_log.write(f'O Insertion Sort levou {time() - tinicio} segundos\n')
    arquivo_log.write(95 * "_")


def get_switch(switch):
    tipo_de_busca = "sequencial"
    text_sort = "Busca Sequencial"
    if switch.value:
        tipo_de_busca = "binaria"
        text_sort = "Busca Binária"

    return tipo_de_busca, text_sort


# def update_img(nome_carro, photos_carros):
#     # Atualiza a imagem do
#     photos_carros.src = f'telas/assets/img/cars/{nome_carro}.png'
#     photos_carros.update()
