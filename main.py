import time

import flet as ft

from Entidades.aluguel import Aluguel
from Entidades.carro import Carro
from Entidades.clientes import Cliente
from Entidades.filial import Filial
from telas.colors import *
from telas.pg_aluguel import criar_aluguel
from telas.pg_dados import data_page
from telas.home import home
from telas.pg_cliente import pg_clientes
from Funcoes.config import config
import time

cliente = Cliente()
carro = Carro()
filial = Filial()
aluguel = Aluguel()
arquivo_cliente = open('Bases/cliente.dat', "r+b")
arquivo_carro = open('Bases/carro.dat', "r+b")
arquivo_filial = open('Bases/filial.dat', "r+b")
arquivo_aluguel = open('Bases/aluguei.dat', "r+b")
arquivo_log = open('Bases/log.txt', "w+")

registro_cliente = []
registro_carro = []
registro_filial = []
registro_aluguel = []
t_inicio = time.time()
tam = 100000
# cliente.criar_base(tam, arquivo=arquivo_cliente, desordenada=True)
# carro.criar_base(tam, arquivo=arquivo_carro, desordenada=True)
# filial.criar_base(tam, arquivo=arquivo_filial, desordenada=True)
# aluguel.criar_base(tam, arquivo=arquivo_aluguel, arquivo_cliente=arquivo_cliente,
#                    arquivo_carro=arquivo_carro, arquivo_filial=arquivo_filial, desordenada=True,
#                    arquivo_log=arquivo_log)
# print("Tempo de criação dos arquivos: ", time.time() - t_inicio)


def main(page: ft.Page):
    page.title = 'Locadora de Carros'
    page.header = 'Locadora de Carros'
    page.bgcolor = fundo()
    page.window.min_width = 1600
    page.window.min_height = 860
    page.window.max_width = 1600
    page.window.max_height = 860
    page.window.width = 1600
    page.window.height = 860
    page.window.maximizable = False
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.padding = 0
    page.margin = 0

    header = ft.Row(
        controls=[
            ft.Column(
                [
                    ft.Text("NOME DA LOCADORA", size=38, weight=ft.FontWeight.BOLD),
                ],
                spacing=0,
                tight=True,
            )
        ]
    )
    content_container = ft.Column(expand=True, spacing=0, )

    tabs = ft.Tabs(
        selected_index=0,
        on_change=lambda e: update_content(e.control.selected_index),
        tabs=[
            ft.Tab(text="Início", icon=ft.Icons.HOME),
            ft.Tab(text="Alugar", icon=ft.Icons.ADD),
            ft.Tab(text="Clientes", icon=ft.Icons.PEOPLE),
            ft.Tab(text="Dados", icon=ft.Icons.BAR_CHART),
        ],
        indicator_border_side=ft.BorderSide(  # Define a borda do indicador
            color=botao_laranja(),  # Cor da borda
            width=5,  # Espessura da borda
        ),
        label_color=botao_laranja(),
        unselected_label_text_style=ft.TextStyle(color=fundo(), size=12, weight=ft.FontWeight.BOLD),
        divider_color=ft.Colors.TRANSPARENT,
    )

    opcoes = ft.Dropdown(
        label='Tipo de busca',
        border_color=texto_padrao(),
        hint_text="Sequencial",
        on_change=lambda e: validar_opcao(e),  # Chama a função para validar a opção
        width=300,
        border_radius=10,

        value='Sequencial',
        options=[
            ft.dropdown.Option("Sequencial"),
            ft.dropdown.Option("Binaria"),
        ],
        error_text="",  # Inicialmente sem erro
        error_style=ft.TextStyle(color=laranja_aviso(), size=12, weight=ft.FontWeight.BOLD),

    )
    sort_bar = ft.Row(controls=[opcoes])

    def validar_opcao(e):
        if e.control.value == "Binaria" and not config.dados_ordenados:
            for i in range(3, 0, -1):
                e.control.error_text = f"Base deve estar ordenada. Retornando em: {i}"
                e.page.update()
                time.sleep(1)
            e.page.update()
            e.control.value = "Sequencial"
            e.control.error_text = ""
            e.page.update()
        else:
            e.control.error_text = ""
            e.control.update()

    def get_pesquisa():
        print(config.dados_ordenados)

        if not config.dados_ordenados:
            return "Sequencial"
        else:
            return opcoes.value

    def update_content(index):
        content_container.controls.clear()

        if index == 0:
            content_container.controls.extend(home(page, arquivo_aluguel, aluguel, arquivo_cliente, cliente,
                                                   arquivo_carro, carro, arquivo_filial, filial, arquivo_log,
                                                   tipo_pesquisa=get_pesquisa()))
        elif index ==1:
            content_container.controls.extend(criar_aluguel(page, arquivo_aluguel, aluguel, arquivo_cliente, cliente,
                                                            arquivo_carro, carro, arquivo_filial, filial, arquivo_log,
                                                            tipo_pesquisa=get_pesquisa(), ))
        elif index == 2:
            content_container.controls.extend(pg_clientes(page, arquivo_cliente, arquivo_log, cliente,
                                                          tipo_pesquisa=get_pesquisa(), ))
        elif index == 3:
            content_container.controls.extend(data_page(page, arquivo_aluguel, aluguel, arquivo_cliente, cliente,
                                                        arquivo_carro, carro, arquivo_filial, filial,
                                                        arquivo_log, dados_ordenados=config.dados_ordenados))
        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    ft.Row(
                        controls=[header, tabs, sort_bar],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=150,

                    ),
                    bgcolor=principal(),
                    padding=ft.Padding(left=30, right=30, top=0, bottom=0),
                    alignment=ft.alignment.center,

                ),
                ft.Container(
                    ft.Column(
                        controls=[content_container],
                        expand=True,  # Expande para ocupar o espaço disponível
                        spacing=0,
                    ),
                ),

            ],
            alignment=ft.MainAxisAlignment.START,  # Alinha os filhos com espaço entre eles
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
            expand=True,  # Expande para ocupar toda a altura da página

        )
    )
    update_content(0)


ft.app(target=main)
