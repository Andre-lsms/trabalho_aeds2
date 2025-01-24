
import math
import struct
from random import randint
from time import time
from Funcoes.pesquiesa import  *
from faker import Faker

fake = Faker('pt_BR')
def tamanho_registro(entidade):
    return struct.calcsize(entidade.get_formato())


def quantidade_registros(arquivo, entidade):
    return entidade.tamanho_arquivo(arquivo) // tamanho_registro(entidade)




def ler_ultimo_registro(arquivo, entidade):
    tamanho = arquivo.tamanho_arquivo(arquivo)
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
    tamanho = entidade.tamanho_arquivo(arquivo)
    total_registros = tamanho // tamanho_registro(entidade)

    for i in range(total_registros - 1, 0, -1):
        j = randint(0, i)

        # Read record i
        arquivo.seek(i * tamanho_registro(entidade))
        registro_i = entidade.ler_registro(arquivo)

        # Read record j
        arquivo.seek(j * tamanho_registro(entidade))
        registro_j = entidade.ler_registro(arquivo)

def gerar_endereco():
    rua = fake.street_name()
    numero = fake.building_number()
    bairro = fake.bairro()
    cidade = fake.city()
    return rua + ', ' + numero + ' - ' + bairro + '. ' + cidade
