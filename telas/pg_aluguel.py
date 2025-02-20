import datetime

import flet as ft

from Entidades import funcoes
from Funcoes.interface_logger import InterfaceLogger
from telas.colors import *
from Funcoes.pesquiesa import *
from Entidades.clientes import Cliente
from Entidades.carro import Carro
from Entidades.filial import Filial
from telas.templates import criar_text_field
from Funcoes.alert import alert, loading

registro_cliente = Cliente()
registro_carro = Carro()
registro_filial = Filial()


def criar_aluguel(page: ft.Page, arquivo_aluguel, aluguel, arquivo_cliente, cliente, arquivo_carro, carro,
                  arquivo_filial, filial, arquivo_log, tipo_pesquisa=''):
    loading_dialog = loading()
    page.dialog = loading_dialog
    loading_dialog.open = False
    page.padding = 0
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color=ft.colors.TRANSPARENT,  # Apenas a cor direta, sem chaves

            track_visibility=True,
            thumb_visibility=True,
            thumb_color=laranja_aviso(),
            thickness=10,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )

    caixa_id_cliente = ft.TextField(
        label='Código: ',
        label_style=ft.TextStyle(color=texto_padrao(), size=14, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        width=250, height=50,
        prefix_text='#',
        disabled=False,
        bgcolor=fundo_neutro(),
        border_radius=10,
        border_width=0,
        autofocus=True,
        input_filter=ft.NumbersOnlyInputFilter(),
        on_submit=lambda e: buscar_cliente(e, tipo_pesquisa, arquivo_log)
    )
    botao_pesquisa_cliente = ft.ElevatedButton(
        text='Buscar',
        color=texto_padrao(),
        bgcolor=botao_laranja(),
        width=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                             text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter',
                                                     weight=ft.FontWeight.BOLD, )),
        height=50,
        on_click=lambda e: buscar_cliente(e, tipo_pesquisa, arquivo_log)
    )
    caixa_id_carro = ft.TextField(
        label='Código',
        label_style=ft.TextStyle(color=texto_padrao(), size=14, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        width=210, height=50,
        prefix_text='#',
        disabled=False,
        bgcolor=fundo_neutro(),
        border_radius=10,
        border_width=0,
        autofocus=True,
        input_filter=ft.NumbersOnlyInputFilter(),
        on_submit=lambda e: buscar_carro(e, tipo_pesquisa, arquivo_log)
    )
    botao_pesquisa_carro = ft.ElevatedButton(
        text='Buscar',
        color=texto_padrao(),
        bgcolor=botao_laranja(),
        width=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                             text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter',
                                                     weight=ft.FontWeight.BOLD, )),
        height=50,
        on_click=lambda e: buscar_carro(e, tipo_pesquisa, arquivo_log)
    )
    caixa_id_filial = ft.TextField(
        label='Código',
        label_style=ft.TextStyle(color=texto_padrao(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        width=250, height=50,
        prefix_text='#',
        disabled=False,
        bgcolor=fundo_neutro(),
        border_radius=10,
        border_width=0,
        autofocus=True,
        input_filter=ft.NumbersOnlyInputFilter(),
        on_submit=lambda e: buscar_filial(e, tipo_pesquisa, arquivo_log)
    )
    botao_pesquisa_filial = ft.ElevatedButton(
        text='Buscar',
        color=texto_padrao(),
        bgcolor=botao_laranja(),
        width=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                             text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter',
                                                     weight=ft.FontWeight.BOLD, )),
        height=50,
        on_click=lambda e: buscar_filial(e, tipo_pesquisa, arquivo_log)
    )
    caixa_id_aluguel = ft.TextField(
        label='Código',
        label_style=ft.TextStyle(color=texto_padrao(), size=12, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        width=250, height=50,
        prefix_text='#',
        disabled=True,
        bgcolor=fundo_neutro(),
        border_radius=10,
        border_width=0,
        autofocus=True,
        input_filter=ft.NumbersOnlyInputFilter(),
        on_submit=lambda e: buscar_filial(e, tipo_pesquisa, arquivo_log)
    )

    caixa_nome_cliente = criar_text_field('Nome', 410, 50)
    caixa_cpf_cliente = criar_text_field('CPF', 200, 50)
    caixa_marca_carro = criar_text_field('Marca', 200, 50)
    caixa_modelo_carro = criar_text_field('Modelo', 200, 50)
    caixa_cor_carro = criar_text_field('Cor', 200, 50)
    caixa_ano_carro = criar_text_field('Ano', 200, 50)
    caixa_status_carro = criar_text_field('Status', 10, 50, align=ft.TextAlign.CENTER)
    caixa_nome_filial = criar_text_field('Nome', 410, 50)
    caixa_email_filial = criar_text_field('Email', 410, 50)
    caixa_valor_diaria = criar_text_field('Valor da diária', 200, 50, prefix_text='R$', disabled=False)
    caixa_data_aluguel = criar_text_field('Data do aluguel', 200, 50)
    caixa_tempo = criar_text_field('Tempo', 200, 50, disabled=False)
    caixa_valor_total = criar_text_field('Valor Total', 200, 50, prefix_text='R$')
    saida = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        cache_extent=1000,
    )
    button_close = ft.ElevatedButton(
        text='Fechar',
        color=botao_laranja(),
        bgcolor=principal(),
        width=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), ),
        height=50,
        on_click=lambda e: column_hide(e),
        visible=False
    )
    interface_logger = InterfaceLogger(saida)
    botao_criar_aluguel = ft.ElevatedButton(
        text='Criar Aluguel',
        color=principal(),
        bgcolor=botao_laranja(),
        width=410,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), ),
        visible=False,
        height=50,
        on_click=lambda e: adicionar_aluguel()
    )
    botao_calcular = ft.ElevatedButton(
        text='Simular valor',
        color=laranja_aviso(),
        bgcolor=botao_branco(),
        width=200,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        height=50,
        on_click=lambda e: calcular_valor(e)
    )
    column_cliente = ft.Container(

        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text('DADOS DO LOCATÁRIO', size=14, weight=ft.FontWeight.BOLD,
                                            color=laranja_aviso()),
                            bgcolor=principal(),
                            width=480,
                            height=30,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                    ]
                ),
                ft.Row(controls=[caixa_id_cliente, botao_pesquisa_cliente]),
                ft.Row(controls=[caixa_nome_cliente, caixa_cpf_cliente]),
            ],
            expand=True,
        ),
        border_radius=10,
        padding=ft.padding.all(10),
        alignment=ft.alignment.center,
        width=500
    )
    column_carro = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text('DADOS DO CARRO', size=14, weight=ft.FontWeight.BOLD,
                                            color=laranja_aviso()),
                            bgcolor=principal(),
                            width=480,
                            height=30,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                    ]
                ),
                ft.Row(controls=[caixa_id_carro, botao_pesquisa_carro,
                                 ft.ElevatedButton(
                                     text='Exibir disponiveis',
                                     color=laranja_aviso(),
                                     bgcolor=botao_branco(),
                                     width=100,
                                     style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10), ),
                                     height=50,
                                     on_click=lambda e: exibir_carros_disponiveis(e),
                                 ), ]),
                ft.Row(controls=[caixa_marca_carro, caixa_modelo_carro]),
                ft.Row(controls=[caixa_cor_carro, caixa_ano_carro]),
                ft.Row(controls=[caixa_status_carro, ], ),
            ],
            expand=True,
        ),
        border_radius=10,
        padding=ft.padding.all(10),
        width=500,
        visible=False,
    )

    column_filial = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text('DADOS DA FILIAL', size=14, weight=ft.FontWeight.BOLD,
                                            color=laranja_aviso()),
                            bgcolor=principal(),
                            width=480,
                            height=30,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                    ]
                ),
                ft.Row(controls=[caixa_id_filial, botao_pesquisa_filial]),
                ft.Row(controls=[caixa_nome_filial]),
                ft.Row(controls=[caixa_email_filial]),
            ],
            expand=True,
        ),
        border_radius=10,
        padding=ft.padding.all(10),
        width=500,
        visible=False,
    )

    column_aluguel = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text('DADOS DO ALUGUEL', size=14, weight=ft.FontWeight.BOLD,
                                            color=laranja_aviso()),
                            bgcolor=principal(),
                            width=480,
                            height=30,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    expand=True,
                ),
                ft.Row(controls=[caixa_id_aluguel, caixa_data_aluguel]),
                ft.Row(controls=[caixa_valor_diaria, caixa_tempo]),
                ft.Row(controls=[botao_calcular, caixa_valor_total]),
                ft.Row(controls=[botao_criar_aluguel]),
            ],
            spacing=30,
            expand=True,
        ),
        border_radius=10,
        padding=ft.padding.all(10),
        width=500,
        visible=False,
    )

    column_carros_disponiveis = ft.Column(
        controls=[
            ft.Container(
                content=ft.Column(controls=[saida, button_close]),
                width=410,
                height=250,
                bgcolor=fundo(),
                border_radius=10,
                border=ft.border.all(1, principal()),

                margin=ft.margin.only(top=10),
                padding=10,

            ),

        ],
        visible=False,
        expand=True,
        width=500,

    )

    column_left = ft.Column(
        controls=[
            ft.Row(controls=[
                ft.Column(controls=[column_cliente, column_carro, column_filial, ]),
                ft.Column(controls=[column_aluguel]),
                column_carros_disponiveis,
            ],
                spacing=50,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),

        ],
        spacing=50,
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def set_id():
        id = funcoes.quantidade_registros(arquivo_aluguel, aluguel)
        id += 1
        caixa_id_aluguel.value = str(id)
        caixa_data_aluguel.value = datetime.datetime.now().strftime('%d/%m/%Y')

    set_id()

    def exibir_carros_disponiveis(e):
        loading_dialog.open = True
        page.update()
        column_carros_disponiveis.visible = True
        saida.clean()
        carro.exibir_disponiveis(arquivo_carro, interface_logger),
        caixa_id_carro.focus()
        button_close.visible = True
        loading_dialog.open = False
        page.update()

    def column_hide(e):
        column_carros_disponiveis.visible = False
        button_close.visible = False
        e.page.update()

    def calcular_valor(e):
        try:
            valor_diaria = int(caixa_valor_diaria.value)
            tempo = int(caixa_tempo.value)
            if valor_diaria > 1000:
                botao_criar_aluguel.visible = False
                page.add(alert(mensagem="O valor máximo é R$1000", icone="ERROR"))
                caixa_valor_diaria.focus()

                return
            if valor_diaria < 100:
                botao_criar_aluguel.visible = False
                page.add(alert(mensagem="O valor mínimo é R$100", icone="ERROR"))
                caixa_valor_diaria.focus()

                return
            if tempo > 30:
                botao_criar_aluguel.visible = False
                page.add(alert(mensagem="O tempo máximo é 30 dias", icone="ERROR"))
                caixa_tempo.focus()
                return
            if tempo <= 0:
                botao_criar_aluguel.visible = False
                page.add(alert(mensagem="O tempo mínimo é 1 dia", icone="ERROR"))
                caixa_tempo.focus()
                return

            caixa_tempo.label = 'Tempo'
            caixa_valor_diaria.label = 'Valor da diária'
            valor_total = int(valor_diaria) * int(tempo)
            caixa_valor_total.value = valor_total
            botao_criar_aluguel.visible = True
            e.page.update()
        except ValueError:
            if caixa_valor_diaria.value == '':
                caixa_valor_diaria.label = 'Digite um número'
                caixa_valor_diaria.focus()
            if caixa_tempo.value == '':
                caixa_tempo.label = 'Digite um número'
                caixa_tempo.focus()

            page.add(alert(mensagem="Digite um numero", icone="ERROR"))

    def buscar_cliente(e, t_busca, log):
        if caixa_id_cliente.value != '':
            loading_dialog.open = True
            page.update()
            id = caixa_id_cliente.value
            try:
                id = int(id)
                if t_busca == 'Binaria':
                    registro = pesquisa_binaria(id, arquivo_cliente, cliente, log)
                else:
                    registro = pesquisa_sequencial(id, arquivo_cliente, cliente, log)
                if registro == -1:
                    limpar_caixas(caixa_nome_cliente)
                    limpar_caixas(caixa_cpf_cliente)
                    column_aluguel.visible = False
                    column_carro.visible = False
                    column_filial.visible = False
                    page.add(alert(mensagem="Cliente não encontrado", icone="ERROR", cor=laranja_aviso()))

                else:
                    caixa_id_cliente.border = 1
                    caixa_nome_cliente.value = registro.nome
                    caixa_cpf_cliente.value = registro.cpf
                    caixa_id_cliente.label = 'Cliente'
                    global registro_cliente
                    registro_cliente = registro
                    column_carro.visible = True
            except ValueError:
                page.add(alert(mensagem="Digite um numero", icone="ERROR"))

            finally:
                loading_dialog.open = False
                page.update()

    def buscar_carro(e, t_busca, log):
        if caixa_id_carro.value != '':
            loading_dialog.open = True
            page.update()
            id = caixa_id_carro.value
            try:
                id = int(id)
                if t_busca == 'Binaria':
                    registro = pesquisa_binaria(id, arquivo_carro, carro, log)
                else:
                    registro = pesquisa_sequencial(id, arquivo_carro, carro, log)

                if registro == -1:
                    limpar_caixas(caixa_marca_carro)
                    limpar_caixas(caixa_modelo_carro)
                    limpar_caixas(caixa_cor_carro)
                    limpar_caixas(caixa_ano_carro)
                    limpar_caixas(caixa_status_carro)
                    column_aluguel.visible = False
                    column_filial.visible = False
                    page.add(alert(mensagem="Carro não encontrado", icone="ERROR"))
                else:
                    caixa_id_carro.border = 1
                    caixa_id_carro.label = 'Carro'
                    caixa_marca_carro.value = registro.marca
                    caixa_modelo_carro.value = registro.modelo
                    caixa_cor_carro.value = registro.cor
                    caixa_ano_carro.value = registro.ano
                    if registro.disponivel:
                        caixa_status_carro.value = 'Disponível'
                        caixa_status_carro.color = laranja_aviso()
                        caixa_status_carro.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD)
                        caixa_status_carro.bgcolor = fundo_neutro_contraste()
                        column_filial.visible = True
                        column_carros_disponiveis.visible = False
                        button_close.visible = False

                    else:
                        caixa_status_carro.value = 'Indisponível'
                        caixa_status_carro.color = texto_padrao()
                        caixa_status_carro.text_style = ft.TextStyle(weight=ft.FontWeight.BOLD)
                        caixa_status_carro.bgcolor = laranja_aviso()
                        column_filial.visible = False
                        column_aluguel.visible = False
                    global registro_carro
                    registro_carro = registro
            except ValueError:
                page.add(alert(mensagem="Digite um numero", icone="ERROR"))
            finally:
                loading_dialog.open = False
                page.update()

    def buscar_filial(e, t_busca, log):
        if caixa_id_filial.value != '':
            loading_dialog.open = True
            page.update()
            id = caixa_id_filial.value
            try:
                id = int(id)
                if t_busca == 'Binaria':
                    registro = pesquisa_binaria(id, arquivo_filial, filial, log)
                else:
                    registro = pesquisa_sequencial(id, arquivo_filial, filial, log)

                if registro == -1:
                    limpar_caixas(caixa_nome_filial)
                    limpar_caixas(caixa_email_filial)
                    column_aluguel.visible = False
                    page.add(alert(mensagem="Filial não encontrada", icone="ERROR"))

                else:
                    caixa_id_filial.label = 'Filial'
                    caixa_nome_filial.value = registro.nome
                    caixa_email_filial.value = registro.email
                    global registro_filial
                    registro_filial = registro
                    column_aluguel.visible = True
            except ValueError:
                page.add(alert(mensagem="Digite um numero", icone="ERROR"))
            finally:
                loading_dialog.open = False
                page.update()

    def adicionar_aluguel():

        global registro_cliente, registro_carro, registro_filial
        try:
            id = aluguel.quantidade_registros(arquivo_aluguel) + 1
            int(registro_cliente.codigo)
            int(registro_carro.codigo)
            id_filial = int(registro_filial.codigo)
            data_aluguel = caixa_data_aluguel.value
            tempo = int(caixa_tempo.value)
            valor_total = int(caixa_valor_total.value)
            diaria = int(caixa_valor_diaria.value)
            try:
                diaria = int(diaria)
                registro = aluguel.criar_registro(id, cliente=registro_cliente, carro=registro_carro,
                                                  filial=registro_filial,
                                                  data_aluguel=data_aluguel, tempo=tempo,
                                                  valor_total=valor_total, diaria=diaria, arquivo_carro=arquivo_carro, )

                aluguel.salvar_registro(arquivo=arquivo_aluguel, registro=registro)
                page.add(alert(mensagem="Aluguel criado com sucesso", icone="done", cor=texto_padrao()))
                limpar_caixas(caixa_id_cliente)
                limpar_caixas(caixa_nome_cliente)
                limpar_caixas(caixa_cpf_cliente)
                limpar_caixas(caixa_id_carro)
                limpar_caixas(caixa_marca_carro)
                limpar_caixas(caixa_modelo_carro)
                limpar_caixas(caixa_cor_carro)
                limpar_caixas(caixa_ano_carro)
                limpar_caixas(caixa_status_carro)
                limpar_caixas(caixa_id_filial)
                limpar_caixas(caixa_nome_filial)
                limpar_caixas(caixa_email_filial)
                limpar_caixas(caixa_valor_diaria)
                limpar_caixas(caixa_data_aluguel)
                limpar_caixas(caixa_tempo)
                limpar_caixas(caixa_valor_total)
                column_aluguel.visible = False
                column_carro.visible = False
                column_filial.visible = False
                column_carros_disponiveis.visible = False
                button_close.visible = False
                botao_criar_aluguel.visible = False
                data_formatada = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                page.open(ft.SnackBar(
                    ft.Row(controls=[
                        ft.Text(f'Aluguel criado com sucesso Codigo: {id}',size=14, weight=ft.FontWeight.BOLD, color=texto_padrao()),
                        ft.Text(f'Data{data_formatada}',size=14, weight=ft.FontWeight.BOLD, color=texto_padrao()),
                    ],
                        spacing=30,
                    ),
                        duration=10000,
                        bgcolor=laranja_aviso()
                    )
                )

            except ValueError:
                page.add(alert(mensagem="Digite um numero", icone="ERROR"))

        except Exception as e:
            page.add(alert(mensagem="Preencha todos os campos", icone="ERROR"))
            print(e)
        carro.status = False
        set_id()
        page.update()

    def limpar_caixas(caixa):
        caixa.value = ''

    return [
        ft.Container(
            ft.Column(
                controls=[
                    ft.Row(controls=[column_left]),

                ],
                spacing=30,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN

            ),
            padding=ft.padding.Padding(left=30, right=0, top=0, bottom=30),
            alignment=ft.alignment.top_center,

        )
    ]
