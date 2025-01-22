import flet as ft

from Entidades import funcoes
from telas.colors import *


def pg_clientes(page: ft.Page, arquivo_cliente, cliente):
    botao_cadastro = ft.ElevatedButton(
        text='Cadastrar',
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50,

        on_click=lambda e: cadastro(),

    )

    caixa_id_cliente = ft.TextField(
        label='Codigo: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        disabled=True,
        border_radius=10,
        bgcolor=cinza_claro(),
        width=190,
        height=50,
    )

    caixa_nome_cliente = ft.TextField(
        label='Nome do cliente: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        border_color=branco(),
        bgcolor=cinza_claro(),
        width=500,
        height=50,
        max_length=30,
    )
    caixa_idade = ft.TextField(
        label='idade: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        bgcolor=cinza_claro(),
        width=500,
        height=50,
        max_length=2,
    )
    caixa_cpf_cliente = ft.TextField(
        label='CPF',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        bgcolor=cinza_claro(),
        width=500,
        height=50,
        on_change=lambda e: formatar_cpf(e)
    )
    # Caixa de texto para o código do carro
    # Botão de buscar

    # Caixa de texto para o nome e cpf do carro (inicialmente vazia) e
    caixa_endereco = ft.TextField(
        label='Endereço: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        bgcolor=cinza_claro(),
        width=500,
        height=50,
        max_length=70,
    )
    caixa_telefone = ft.TextField(
        label='Telefone: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        bgcolor=cinza_claro(),
        width=500,
        height=50,
        max_length=20
    )
    caixa_email = ft.TextField(
        label='Email:',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        bgcolor=cinza_claro(),
        width=500,
        height=50,
        max_length=30
    )


    column_left = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    caixa_id_cliente,
                ],
            ),
            ft.Row(
                controls=[
                    caixa_nome_cliente,
                ],
            ),
            ft.Row(
                controls=[
                    caixa_cpf_cliente
                ],
            ),
            ft.Row(
                controls=[
                    caixa_idade,
                ]

            ), ft.Row(
                controls=[
                    caixa_endereco,
                ]

            ),
            ft.Row(
                controls=[
                    caixa_telefone,
                ]
            ),
            ft.Row(
                controls=[
                    caixa_email,
                ]
            ),
            ft.Row(
                controls=[
                    botao_cadastro
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
        ],

    )

    def set_id():
        id = funcoes.quantidade_registros(arquivo_cliente, cliente)
        id += 1
        caixa_id_cliente.value = str(id)

    set_id()

    def formatar_cpf(e):
        texto = ''.join(filter(str.isdigit, e.control.value))
        texto = texto[:11]
        # Aplica a formatação de CPF
        if len(texto) > 9:
            texto_formatado = f"{texto[:3]}.{texto[3:6]}.{texto[6:9]}-{texto[9:]}"
        elif len(texto) > 6:
            texto_formatado = f"{texto[:3]}.{texto[3:6]}.{texto[6:]}"
        elif len(texto) > 3:
            texto_formatado = f"{texto[:3]}.{texto[3:]}"
        else:
            texto_formatado = texto

        # Atualiza o valor do campo com o texto formatado
        e.control.value = texto_formatado
        e.page.update()

    def cadastro():
        try:
            id = int(caixa_id_cliente.value)
            nome = caixa_nome_cliente.value
            idade = int(caixa_idade.value)
            cpf = caixa_cpf_cliente.value
            endereco = caixa_endereco.value
            telefone = caixa_telefone.value
            email = caixa_email.value
            cliente.salvar_registro(arquivo_cliente, cliente.criar_registro(id, nome=nome, idade=idade, cpf=cpf,
                                                                            endereco=endereco, telefone=telefone,
                                                                            email=email))
            set_id()
            caixa_nome_cliente.value = ''
            caixa_idade.value = ''
            caixa_cpf_cliente.value = ''
            caixa_endereco.value = ''
            caixa_telefone.value = ''
            caixa_email.value = ''
            alert_dialog = ft.AlertDialog(
                icon=ft.Icon(name="CHECK", color=branco(), ),
                title=ft.Text("Cliente cadastrado com sucesso", color=branco(), size=20, weight=ft.FontWeight.BOLD,
                              text_align=ft.TextAlign.CENTER),

                bgcolor=verde_escuro(),
                open=True,
            )
        except:
            alert_dialog = ft.AlertDialog(
                icon=ft.Icon(name="ERROR", color=branco(), ),
                title=ft.Text("Insira todos os dados", color=branco(), size=20, weight=ft.FontWeight.BOLD,
                              text_align=ft.TextAlign.CENTER),

                bgcolor=verde_escuro(),

                open=True
            )
        page.add(alert_dialog)
        page.update()

    return [
        ft.Container(
            ft.Row(
                controls=[
                    column_left,
                ],

            ),
            padding=ft.padding.all(30)
        )
    ]
