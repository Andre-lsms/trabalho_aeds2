import flet as ft

from Entidades import funcoes
from Entidades.aluguel import Aluguel
from Entidades.carro import Carro
from Entidades.clientes import Cliente
from Entidades.filial import Filial
from Funcoes.pesquiesa import *
from telas.colors import *

cliente = Cliente()
carro = Carro()
filial = Filial()
aluguel = Aluguel()

def home(page: ft.Page, arquivo_aluguel, aluguel, arquivo_cliente, cliente, arquivo_carro, carro,
         arquivo_filial, filial, arquivo_log, ):

    caixa_pesquisa_aluguel = ft.TextField(
        label='Pesquisar Aluguel',
        border_color=branco(),
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        align_label_with_hint=True,
        text_align=ft.TextAlign.CENTER,
        width=250,
        height=50,
        border_radius=10,
        prefix_text='#',
        prefix_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
    )
    botao_pesquisa = ft.ElevatedButton(
        text='get_switch(switch)[1]',
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50,
        on_click=lambda e: busca(e,)
    )

    caixa_id_cliente = ft.TextField(
        label='Codigo: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=150,
        height=50,
        prefix_text='#',
        prefix_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
    )
    caixa_nome_cliente = ft.TextField(
        label='Nome do locatário: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )
    caixa_idade_cliente = ft.TextField(
        label='Idade: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=150,
        height=50,
    )
    caixa_cpf_cliente = ft.TextField(
        label='CPF',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )
    caixa_endereco_cliente = ft.TextField(
        label='Endereço: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=410,
        height=50,
    )
    caixa_telefone_cliente = ft.TextField(
        label='Telefone: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )
    caixa_email_cliente = ft.TextField(
        label='Email: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )

    caixa_id_carro = ft.TextField(
        label='Codigo: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=150,
        height=50,
        prefix_text='#',
        prefix_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
    )
    caixa_placa_carro = ft.TextField(
        label='Placa:',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )
    caixa_marca_carro = ft.TextField(
        label='Marca: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )
    caixa_modelo_carro = ft.TextField(
        label='Modelo: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=150,
        height=50,
    )
    caixa_cor_carro = ft.TextField(
        label='Cor: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )
    caixa_ano_carro = ft.TextField(
        label='Ano: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=150,
        height=50,
    )

    caixa_valor_diaria = ft.TextField(
        label='Valor da diária: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
        prefix_text='R$ ',
        prefix_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, )
    )

    caixa_id_filial = ft.TextField(
        label='Codigo: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=150,
        height=50,
        prefix_text='#',
        prefix_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
    )
    caixa_nome_filial = ft.TextField(
        label='Filial de saida: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )
    caixa_endereco_filial = ft.TextField(
        label='Endereço: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=410,
        height=50,
    )
    caixa_telefone_filial = ft.TextField(
        label='Telefone: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )
    caixa_email_filial = ft.TextField(
        label='Email: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=250,
        height=50,
    )

    column_info = ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text('DADOS DO LOCATÁRIO', size=20, weight=ft.FontWeight.BOLD,
                                                color=branco()),
                                bgcolor=verde_escuro(),
                                width=410,
                                height=30,
                                border_radius=5,
                                alignment=ft.alignment.center,
                            ),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            caixa_nome_cliente, caixa_id_cliente
                        ],
                    ),
                    ft.Row(
                        controls=[
                            caixa_cpf_cliente, caixa_idade_cliente
                        ],
                    ),
                    ft.Row(
                        controls=[
                            caixa_telefone_cliente
                        ],
                    ),                    ft.Row(
                        controls=[
                            caixa_email_cliente
                        ],
                    ),
                    ft.Row(
                        controls=[
                            caixa_endereco_cliente,
                        ],
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text('DADOS DO CARRO', size=20, weight=ft.FontWeight.BOLD, color=branco()),
                                bgcolor=verde_escuro(),
                                width=410,
                                height=30,
                                border_radius=5,
                                alignment=ft.alignment.center,
                            ),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            caixa_placa_carro, caixa_id_carro
                        ]
                    ),
                    ft.Row(
                        controls=[
                            caixa_marca_carro, caixa_modelo_carro,
                        ],

                    ),
                    ft.Row(
                        controls=[
                            caixa_cor_carro, caixa_ano_carro
                        ],
                    ),

                ]
            ),
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text('DADOS DA FILIAL', size=20, weight=ft.FontWeight.BOLD, color=branco()),
                                bgcolor=verde_escuro(),
                                width=410,
                                height=30,
                                border_radius=5,
                                alignment=ft.alignment.center,
                            ),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            caixa_nome_filial, caixa_id_filial
                        ],
                        expand=True
                    ),
                    ft.Row(
                        controls=[
                            caixa_telefone_filial
                        ],
                        expand=True
                    ),
                    ft.Row(
                        controls=[
                            caixa_email_filial,
                        ],
                        expand=True
                    ),
                    ft.Row(
                        controls=[
                            caixa_endereco_filial
                        ],
                        expand=True
                    ),
                    ft.Row(
                        controls=[
                            caixa_valor_diaria,
                        ]
                    ),
                ],
                expand=True
            )
        ],
        spacing=30,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    photos_carros = ft.Image(
        src="telas/assets/img/cars/default.png",
        error_content=ft.Text('Erro ao carregar imagem'),
        fit=ft.ImageFit.CONTAIN,
        width=600,
    )

    column_left = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    caixa_pesquisa_aluguel,
                    botao_pesquisa,
                ]
            ),
            ft.Container(
                content=column_info,
                margin=ft.margin.only(top=0),
                expand=True,

            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True,
        spacing=20,
    )
    column_right = ft.Column(
        controls=[
            ft.Container(
                content=photos_carros,
                margin=ft.margin.only(top=20),
                padding=ft.padding.all(20),
                expand=True
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        expand=True,
    )

    def update_img(nome_carro):
        photos_carros.src = f'telas/assets/img/cars/{nome_carro}.png'
        photos_carros.update()

    def busca(e, t_busca):
        if caixa_pesquisa_aluguel.value != '':
            carro_busca = Carro()
            cliente_busca = Cliente()
            filial_busca = Filial()
            id = caixa_pesquisa_aluguel.value
            try:
                id = int(id)
                
                if t_busca == 'binaria':
                    registro = pesquisa_binaria(id, arquivo_aluguel, aluguel, arquivo_log)
                    if registro != -1:
                        cliente_busca = funcoes.pesquisa_binaria(registro.codigo, arquivo_cliente, cliente, arquivo_log)
                        carro_busca = funcoes.pesquisa_binaria(registro.codigo, arquivo_carro, carro, arquivo_log)
                        filial_busca = pesquisa_binaria(registro.codigo, arquivo_filial, filial, arquivo_log)
                else:
                    registro = pesquisa_sequencial(id, arquivo_aluguel, aluguel, arquivo_log)
                    if registro != -1:
                        cliente_busca = pesquisa_sequencial(registro.codigo, arquivo_cliente, cliente, arquivo_log)
                        carro_busca = pesquisa_sequencial(registro.codigo, arquivo_carro, carro, arquivo_log)
                        filial_busca = pesquisa_sequencial(registro.codigo, arquivo_filial, filial, arquivo_log)

                if registro == -1:
                    caixa_pesquisa_aluguel.label = 'não encontrado'
                    caixa_pesquisa_aluguel.border = 10
                    caixa_pesquisa_aluguel.color = vermelho()
                    limpar_caixas(caixa_nome_cliente)
                    limpar_caixas(caixa_id_cliente)
                    limpar_caixas(caixa_cpf_cliente)
                    limpar_caixas(caixa_idade_cliente)
                    limpar_caixas(caixa_endereco_cliente)
                    limpar_caixas(caixa_telefone_cliente)
                    limpar_caixas(caixa_email_cliente)
                    limpar_caixas(caixa_id_carro)
                    limpar_caixas(caixa_marca_carro)
                    limpar_caixas(caixa_modelo_carro)
                    limpar_caixas(caixa_cor_carro)
                    limpar_caixas(caixa_ano_carro)
                    limpar_caixas(caixa_placa_carro)
                    limpar_caixas(caixa_valor_diaria)
                    limpar_caixas(caixa_id_filial)
                    limpar_caixas(caixa_nome_filial)
                    limpar_caixas(caixa_endereco_filial)
                    limpar_caixas(caixa_telefone_filial)
                    limpar_caixas(caixa_email_filial)
                    update_img("default")
                else:
                    caixa_pesquisa_aluguel.label = 'Cliente'
                    caixa_pesquisa_aluguel.border = 5
                    caixa_pesquisa_aluguel.border_color = branco()
                    caixa_pesquisa_aluguel.color = branco()


                    # Cliente
                    caixa_id_cliente.value = cliente_busca.codigo
                    caixa_nome_cliente.value = cliente_busca.nome
                    caixa_idade_cliente.value = cliente_busca.idade
                    caixa_cpf_cliente.value = cliente_busca.cpf
                    caixa_email_cliente.value = cliente_busca.email
                    caixa_telefone_cliente.value = cliente_busca.telefone
                    caixa_endereco_cliente.value = cliente_busca.endereco

                    # Carro
                    caixa_id_carro.value = carro_busca.codigo
                    caixa_placa_carro.value = carro_busca.placa
                    caixa_marca_carro.value = carro_busca.marca
                    caixa_modelo_carro.value = carro_busca.modelo
                    caixa_cor_carro.value = carro_busca.cor
                    caixa_ano_carro.value = carro_busca.ano

                    # Filial

                    caixa_id_filial.value = filial_busca.codigo
                    caixa_nome_filial.value = filial_busca.nome
                    caixa_email_filial.value = filial_busca.email
                    caixa_telefone_filial.value = filial_busca.telefone
                    caixa_endereco_filial.value = filial_busca.endereco

                    # Preço
                    caixa_valor_diaria.value = registro.diaria

                    if carro_busca.modelo != '':
                        update_img(carro_busca.modelo)
                    else:
                        update_img("Default")
                    e.page.update()

            except ValueError:
                caixa_pesquisa_aluguel.label = 'Digite um número'
                caixa_pesquisa_aluguel.border_color = vermelho()

        e.page.update()

    def limpar_caixas(caixa):
        caixa.value = ''

    return [
        ft.Container(
            ft.Row(
                controls=[
                    column_left,column_right,
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,

                expand=True
            ),
            padding=ft.padding.all(0),
            margin=ft.margin.only(left=30),
            expand=True
        )
    ]
