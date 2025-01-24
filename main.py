import flet as ft

from Entidades.aluguel import Aluguel
from Entidades.carro import Carro
from Entidades.clientes import Cliente
from Entidades.filial import Filial
from Entidades.funcoes import *
from telas.colors import *
from telas.criar_aluguel import criar_aluguel
from telas.data_page import data_page
from telas.home import home
from telas.pg_cliente import pg_clientes

width, height = retornar_tamanho_tela()
cliente = Cliente()
carro = Carro()
filial = Filial()
aluguel = Aluguel()
arquivo_cliente = open('Bases/cliente.dat', "w+b")
arquivo_carro = open('Bases/carro.dat', "w+b")
arquivo_filial = open('Bases/filial.dat', "w+b")
arquivo_aluguel = open('Bases/aluguei.dat', "w+b")
arquivo_log = open('Bases/log.txt', "w+")
registro_cliente = []
registro_carro = []
registro_filial = []
registro_aluguel = []

cliente.criar_base(1000, arquivo=arquivo_cliente, desordenada=False)
carro.criar_base(1000, arquivo=arquivo_carro, desordenada=False)
filial.criar_base(1000, arquivo=arquivo_filial, desordenada=False)

aluguel.criar_base(1000, arquivo=arquivo_aluguel, arquivo_cliente=arquivo_cliente,
                   arquivo_carro=arquivo_carro, arquivo_filial=arquivo_filial, desordenada=False,
                   arquivo_log=arquivo_log)


def main(page: ft.Page):
    page.title = 'Locadora de Carros'
    page.header = 'Locadora de Carros'
    page.bgcolor = cinza_escuro()
    page.window.resizable = True
    page.window.maximizable = True
    page.window.minimizable = True
    page.window.maximized = False
    page.window.width = width * 0.90
    page.window.height = height * 0.90
    page.window.min_width = width * 0.90

    page.window.min_height = height * 0.90
    page.window.max_width = width
    page.window.max_height = height
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.padding = 0

    header = ft.Row(
        controls=[
            ft.Text("Nome da Ferramenta", size=38, weight=ft.FontWeight.BOLD),
        ],
        height=130,
        scale=1.1,
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    content_container = ft.Column(expand=True, spacing=0)





    def update_content(index,):
        content_container.controls.clear()
        if index == 0:
            content_container.controls.extend(
                home(page, arquivo_aluguel, aluguel, arquivo_cliente, cliente,
                     arquivo_carro, carro, arquivo_filial, filial, arquivo_log,
                     ))
        elif index == 1:
            content_container.controls.extend(criar_aluguel(page, arquivo_aluguel, aluguel, arquivo_cliente, cliente,
                                                            arquivo_carro, carro, arquivo_filial, filial, arquivo_log,
                                                            ))
        elif index == 2:
            content_container.controls.extend(pg_clientes(page, arquivo_cliente, cliente))
        elif index == 3:
            content_container.controls.extend(data_page(page, arquivo_aluguel, aluguel, arquivo_cliente, cliente,
                                                        arquivo_carro, carro, arquivo_filial, filial,
                                                        arquivo_log))
        page.update()

    tabs = ft.Tabs(
        selected_index=0,
        on_change=lambda e: update_content(e.control.selected_index),
        tabs=[
            ft.Tab(text='Home', icon='home', icon_margin=5),
            ft.Tab(text='Criar Aluguel', icon='add', icon_margin=5),
            ft.Tab(text='Clientes', icon='PERSON_ADD', icon_margin=5),
            ft.Tab(text='Dados', icon='data_usage', icon_margin=5),
        ],
        indicator_border_side=ft.BorderSide(  # Define a borda do indicador
            color=branco(),  # Cor da borda
            width=5,  # Espessura da borda
        ),
        indicator_border_radius=3,
        unselected_label_text_style=ft.TextStyle(color=branco(), size=12, weight=ft.FontWeight.BOLD),
        divider_color=ft.Colors.TRANSPARENT,
        label_color=branco(),
        scale=1.09

        # indicator_tab_size=,

    )

    page.add(
        ft.Container(
            ft.Row(
                controls=[
                    header, tabs
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),

            bgcolor=verde_escuro(),
            padding=ft.Padding(left=30, right=30, top=0, bottom=0),

        ),
        ft.Container(
            ft.Row(
                controls=[
                    ft.Text("Tipo de Busca: ", size=12, weight=ft.FontWeight.BOLD, color=branco()),
                ],

            ),
            padding=ft.Padding(left=30, right=30, top=0, bottom=0),

        ),
        ft.Container(
            ft.Column(
                controls=[

                    content_container,
                ],
                expand=True,

            ),
        ),

    )
    update_content(0)


ft.app(target=main)
