import flet as ft

from Entidades import funcoes
from Entidades.funcoes import get_switch
from telas.colors import *

registro_cliente = []
regoistro_carro = []
registro_filial = []


def criar_aluguel(page: ft.Page, arquivo_aluguel, aluguel, arquivo_cliente, cliente, arquivo_carro, carro,
                  arquivo_filial, filial, arquivo_log, switch):
    botao_buscar_cliente = ft.FilledButton(
        text="Buscar",
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=40,
        on_click=lambda e: buscar_cliente(e, get_switch(switch)[0])
    )
    botao_buscar_carro = ft.FilledButton(
        text='Buscar',
        color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=40,
        on_click=lambda e: buscar_carro(e, get_switch(switch)[0])
    )

    botao_buscar_filial = ft.FilledButton(
        text='Buscar', color=branco(), bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=40,
        on_click=lambda e: buscar_filial(e, get_switch(switch)[0])
    )
    botao_criar_aluguel = ft.FilledButton(
        text='Criar Aluguel', color=branco(),
        bgcolor=verde_escuro(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=40,
        on_click=lambda e: adicionar_aluguel(e.page, registro_cliente, regoistro_carro, registro_filial,
                                             caixa_valor_diaria))
    caixa_id_aluguel = ft.TextField(
        label='Codigo: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        bgcolor=cinza_claro(),
        width=150,
        height=50,
        disabled=True,
    )
    caixa_id_cliente = ft.TextField(
        label='Codigo: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        width=150,
        height=50,
    )

    caixa_nome_cliente = ft.TextField(
        label='Nome do locatário: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=400,
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
        width=400,
        height=50,
    )
    # Caixa de texto para o código do carro
    caixa_id_carro = ft.TextField(
        label='Codigo: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        width=150,
        height=50,
    )
    # Botão de buscar

    # Caixa de texto para o nome e cpf do carro (inicialmente vazia) e
    caixa_marca_carro = ft.TextField(
        label='Marca: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=195,
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
        width=195,
        height=50,
    )
    caixa_placa_carro = ft.TextField(
        label='Placa:',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=195,
        height=50,
    )

    caixa_valor_diaria = ft.TextField(
        label='Valor da diária: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        bgcolor=cinza_claro(),
        width=195,
        height=50,
    )

    caixa_id_filial = ft.TextField(
        label='Código da filial: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_color=branco(),
        border_radius=10,
        width=150,
        height=50,
    )

    caixa_nome_filial = ft.TextField(
        label='Nome: ',
        label_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=branco(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        disabled=True,
        bgcolor=cinza_claro(),
        width=400,
        height=50,
    )


    column_left = ft.Column(
        controls=[

            ft.Container(
                content=ft.Text('DADOS DO LOCATÁRIO', size=20, weight=ft.FontWeight.BOLD, color=branco()),
                bgcolor=verde_escuro(),
                width=400,
                height=30,
                border_radius=5,
                alignment=ft.alignment.center,
            ),
            ft.Row(
                controls=[
                    caixa_id_cliente, botao_buscar_cliente
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


        ],
    )
    column_center = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text('DADOS DA FILIAL', size=20, weight=ft.FontWeight.BOLD, color=branco()),
                bgcolor=verde_escuro(),
                width=400,
                height=30,
                border_radius=5,
                alignment=ft.alignment.center,
            ),
            ft.Row(
                controls=[
                    caixa_id_filial, botao_buscar_filial
                ]
            ), ft.Row(
                controls=[
                    caixa_nome_filial,
                ]
            ),
        ]
    )
    column_right = ft.Column(
        controls=[
            ft.Container(
                content=ft.Text("DADOS DO CARRO", size=20, weight=ft.FontWeight.BOLD, color=branco()),
                bgcolor=verde_escuro(),
                width=400,
                height=30,
                border_radius=5,
                alignment=ft.alignment.center,
            ),
            ft.Row(
                controls=[
                    caixa_id_carro, botao_buscar_carro
                ]
            ),
            ft.Row(
                controls=[
                    caixa_marca_carro, caixa_modelo_carro,
                ]

            ),
            ft.Row(
                controls=[
                    caixa_placa_carro,
                ]
            ),
            ft.Container(
                content=ft.Text("DADOS DO ALUGUEL", size=20, weight=ft.FontWeight.BOLD, color=branco()),
                bgcolor=verde_escuro(),
                width=400,
                height=30,
                border_radius=5,
                alignment=ft.alignment.center,
            ),
            ft.Row(
                controls=[
                    caixa_valor_diaria,
                ]

            ),            ft.Row(
                controls=[
                    caixa_id_aluguel, botao_criar_aluguel
                ]

            ),

        ],

    )


    def set_id():
        id = funcoes.quantidade_registros(arquivo_aluguel, aluguel)
        id += 1
        caixa_id_aluguel.value = str(id)

    set_id()

    def buscar_cliente(e, t_busca):
        # Verificando se o código do cliente foi preenchido
        # Lógica fictícia de busca (por exemplo, se o código do cliente for "123", o nome será "João")
        if caixa_id_cliente.value != '':
            id = caixa_id_cliente.value
            try:
                id = int(id)
                if t_busca == 'binaria':
                    registro = funcoes.pesquisa_binaria(id, arquivo_aluguel, aluguel, arquivo_log)
                else:
                    registro = funcoes.pesquisa_sequencial(id, arquivo_cliente, cliente, arquivo_log)
                if registro == -1:
                    caixa_nome_cliente.value = ''
                    caixa_cpf_cliente.value = ''
                    caixa_id_cliente.label = 'não encontrado'
                    caixa_id_cliente.border_color = vermelho()
                    caixa_id_cliente.color = vermelho()
                    caixa_id_cliente.border = 5

                else:
                    caixa_id_cliente.border_color = branco()
                    caixa_id_cliente.color = branco()
                    caixa_nome_cliente.value = registro[1].decode('utf-8').rstrip(chr(0))
                    caixa_cpf_cliente.value = registro[3].decode('utf-8').rstrip(chr(0))
                    caixa_id_cliente.label = 'Cliente'
                    global registro_cliente
                    registro_cliente = registro
            except ValueError:
                caixa_id_cliente.border_color = vermelho()
                caixa_id_cliente.label = 'Digite um número'

        e.page.update()

    def buscar_carro(e, t_busca):
        if caixa_id_carro.value != '':
            id = caixa_id_carro.value
            try:
                id = int(id)
                if t_busca == 'binaria':
                    registro = funcoes.pesquisa_binaria(id, arquivo_carro, carro, arquivo_log)
                else:
                    registro = funcoes.pesquisa_sequencial(id, arquivo_carro, carro, arquivo_log)

                if registro == -1:
                    caixa_marca_carro.value = ''
                    caixa_modelo_carro.value = ''
                    caixa_placa_carro.value = ''
                    caixa_id_carro.label = 'não encontrado'
                    caixa_id_carro.color = vermelho()
                    caixa_id_carro.border_color = vermelho()
                    caixa_id_carro.border = 5
                else:
                    caixa_id_carro.color = branco()
                    caixa_id_carro.border_color = branco()
                    caixa_id_carro.label = 'Carro'
                    caixa_marca_carro.value = registro[2].decode('utf-8').rstrip(chr(0))
                    caixa_modelo_carro.value = registro[3].decode('utf-8').rstrip(chr(0))
                    caixa_placa_carro.value = registro[1].decode('utf-8').rstrip(chr(0))
                    global regoistro_carro
                    regoistro_carro = registro
            except ValueError:
                caixa_id_carro.border_color = vermelho()
                caixa_id_carro.label = 'Digite um número'

        e.page.update()

    def buscar_filial(e, t_busca):
        if caixa_id_filial.value != '':
            id = caixa_id_filial.value
            try:
                id = int(id)
                if t_busca == 'binaria':
                    registro = funcoes.pesquisa_binaria(id, arquivo_filial, filial, arquivo_log)
                else:
                    registro = funcoes.pesquisa_sequencial(id, arquivo_filial, filial, arquivo_log)


                if registro == -1:
                    caixa_nome_filial.value = ''
                    caixa_id_filial.label = 'não encontrado'
                    caixa_id_filial.color = vermelho()
                    caixa_id_filial.border_color = vermelho()
                    caixa_id_filial.border = 5
                else:
                    caixa_id_filial.color = branco()
                    caixa_id_filial.border_color = branco()
                    caixa_id_filial.label = 'Filial'
                    caixa_nome_filial.value = registro[1].decode('utf-8').rstrip(chr(0))
                    global registro_filial
                    registro_filial = registro
            except ValueError:
                caixa_id_filial.border_color = vermelho()
                caixa_id_filial.label = 'Digite um número'

        e.page.update()

    def adicionar_aluguel(pagina, reg_cliente, reg_carro, reg_filial, caixa_valor_diaria):
        try:
            pegar_id = funcoes.ler_ultimo_registro(arquivo_aluguel, aluguel)
            if pegar_id is None:
                id = 1
            else:
                id = pegar_id[0] + 1
            id_cliente = reg_cliente[0]
            id_carro = reg_carro[0]
            id_filial = reg_filial[0]
            diaria = caixa_valor_diaria.value
            try:
                diaria = int(diaria)
                registro = aluguel.criar_registro(id, id_cliente=id_cliente, id_carro=id_carro, id_filial=id_filial,
                                                  diaria=diaria,
                                                  arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                                                  arquivo_filial=arquivo_filial)

                aluguel.salvar_registro(arquivo=arquivo_aluguel, registro=registro)
                alert_dialog = ft.AlertDialog(
                    icon=ft.Icon(name="CHECK", color=branco(), ),
                    title=ft.Text("Aluguel cadastrado com sucesso", color=branco(), size=20, weight=ft.FontWeight.BOLD,
                                  text_align=ft.TextAlign.CENTER),

                    bgcolor=verde_escuro(),
                    open=True, )
            except ValueError:
                alert_dialog = ft.AlertDialog(
                    icon=ft.Icon(name="ERROR", color=branco(), ),
                    title=ft.Text("Valor inválido", color=branco(), size=20, weight=ft.FontWeight.BOLD,
                                  text_align=ft.TextAlign.CENTER),

                    bgcolor=verde_escuro(),
                    open=True,
                )

        except IndexError:
            alert_dialog = ft.AlertDialog(
                icon=ft.Icon(name="ERROR", color=branco(), ),
                title=ft.Text("Insira todos os dados", color=branco(), size=20, weight=ft.FontWeight.BOLD,
                              text_align=ft.TextAlign.CENTER),

                bgcolor=verde_escuro(),
                open=True,
            )

        page.add(alert_dialog)
        page.update()

    return [
        ft.Container(
            ft.Row(
                controls=[
                    column_left,column_center, column_right
                ],
                spacing=80,
                vertical_alignment=ft.CrossAxisAlignment.START,


            ),
            padding=ft.padding.Padding(left=30, right=30, top=0, bottom=30),
            alignment=ft.alignment.top_center,

        )
    ]
