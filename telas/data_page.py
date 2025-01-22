import flet as ft
from Entidades.funcoes import *
from telas.colors import *
from interface_logger import InterfaceLogger

def data_page(page: ft.Page, arquivo_aluguel, aluguel, arquivo_cliente, cliente, arquivo_carro, carro,
              arquivo_filial, filial,arquivo_log):
    nome_log = ft.Text(
        size=20,
        weight=ft.FontWeight.BOLD,
        color=branco(),
    )
    log_box = ft.TextField(
        multiline=True,
        expand=False,
        read_only=True,
        width=600,
        autofocus=True,

        height=600,
        max_length=600,
        border_color=ft.Colors.TRANSPARENT,
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', ),
    )
    interface_logger = InterfaceLogger(log_box)
    def open_log(arquivo_log):
        log_box.value = ""
        log_box.update()
        nome_log.value = "LOG"
        log_box.update()
        log_box.value = ler_log(arquivo_log, interface_logger)
    def update_data():
        num_clientes = cliente.num_registros(arquivo_cliente)
        num_carros = carro.num_registros(arquivo_carro)
        num_filiais = filial.num_registros(arquivo_filial)
        num_alugueis = aluguel.num_registros(arquivo_aluguel)
        return num_clientes, num_carros, num_filiais, num_alugueis

    def imprimir_base(entidade, arquivo, nome):
        log_box.value = ""
        log_box.update()
        nome_log.value = nome
        page.update()
        entidade.imprimir_base(arquivo,interface_logger)

    update_data()
    button_clientes = ft.ElevatedButton(
        text="Exibir",
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50,
        on_click=lambda e: imprimir_base(cliente, arquivo_cliente, "CLIENTES"),
    )
    button_carros = ft.ElevatedButton(
        text="Exibir",
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50,
        on_click=lambda e: imprimir_base(carro, arquivo_carro, "CARROS"),
    )
    button_filias = ft.ElevatedButton(
        text="Exibir",
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50,
        on_click=lambda e: imprimir_base(filial, arquivo_filial, "FILIAIS"),
    )
    button_alugueis = ft.ElevatedButton(
        text="Exibir",
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50,
        on_click=lambda e: imprimir_base(aluguel, arquivo_aluguel, "ALUGUEIS"),
    )
    button_log = ft.ElevatedButton(
        text="Log",
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50,
        on_click=lambda e: open_log(arquivo_log),
    )

    content = ft.Column(
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Clientes:", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{update_data()[0]}", size=16, weight=ft.FontWeight.BOLD, color=verde_escuro()),

                        ],

                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente no Row
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza os elementos verticalmente no Row
                    ),
                    button_clientes,

                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo vertical do Column
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo horizontal do Column
                width=125,
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Carros:", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{update_data()[1]}", size=16, weight=ft.FontWeight.BOLD, color=verde_escuro()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente no Row
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza os elementos verticalmente no Row
                    ),
                    button_carros,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo vertical do Column
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo horizontal do Column
                width=125,
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Filiais:", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{update_data()[2]}", size=16, weight=ft.FontWeight.BOLD, color=verde_escuro()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente no Row
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza os elementos verticalmente no Row
                    ),
                    button_filias,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo vertical do Column
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo horizontal do Column
                width=125,
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Alugueis:", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{update_data()[3]}", size=16, weight=ft.FontWeight.BOLD, color=verde_escuro()),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza os elementos horizontalmente no Row
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza os elementos verticalmente no Row
                    ),
                    button_alugueis,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo vertical do Column
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo horizontal do Column
                width=125,
            ),
            ft.Column(
                controls=[
                    button_log,
                ],
                alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo vertical do Column
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo horizontal do Column
                width=125,
            ),

        ],
        spacing=50,

    )

    column_left = ft.Column(
        controls=[
            content
        ],
        alignment=ft.MainAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo vertical do Column
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centraliza o conteúdo no eixo horizontal do Column
    )
    column_right = ft.Column(
        controls=[
            ft.Container(
                ft.Column(
                    controls=[
                        ft.Container(
                            content=nome_log,
                            bgcolor=verde_escuro(),
                            border=ft.border.all(1, "white", ),
                            border_radius=ft.border_radius.only(top_left=10, top_right=10),
                            width=600,
                            height=50,  # Define a altura para ver o alinhamento
                            alignment=ft.alignment.center,  # Centraliza o conteúdo no Container
                        ),
                        ft.Container(
                            content=log_box,
                            width=600,
                        )

                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                border=ft.border.all(1, "white", ),
                border_radius=10,
            )
        ]
    )
    return [
        ft.Container(
            ft.Row(
                controls=[
                    column_left,
                    column_right
                ],
                spacing=150,

            ),

            padding=ft.padding.all(30),
            margin=ft.margin.only(left=30)
        )
    ]
