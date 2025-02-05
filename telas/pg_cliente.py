import flet as ft

from Entidades import funcoes
from Funcoes.alert import alert, loading
from Funcoes.pesquiesa import *
from telas.colors import *
from telas.templates import criar_text_field

registro = None


def pg_clientes(page: ft.Page, arquivo_cliente, arquivo_log, cliente, tipo_pesquisa):
    loading_dialog = loading()

    caixa_pesquisa = ft.TextField(
        label='Código do aluguel',
        label_style=ft.TextStyle(color=texto_padrao(), size=14, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter', weight=ft.FontWeight.BOLD, ),
        text_align=ft.TextAlign.CENTER,
        width=250, height=50,
        prefix_text='#',
        disabled=False,
        bgcolor=fundo_neutro(),
        on_submit=lambda e: busca(e, tipo_pesquisa, arquivo_log),
        border_radius=10,
        border_width=0,
        autofocus=True,
        input_filter=ft.NumbersOnlyInputFilter(),
    )
    botao_pesquisa = ft.ElevatedButton(
        text='Buscar',
        color=texto_padrao(),
        bgcolor=botao_laranja(),
        width=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                             text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter',
                                                     weight=ft.FontWeight.BOLD, )),

        height=50,
        on_click=lambda e: busca(e, tipo_pesquisa, arquivo_log),
    )
    caixa_id_cliente = criar_text_field('Código', 200, 80, prefix_text='#')
    caixa_nome_cliente = criar_text_field('Nome', 410, 80)
    caixa_idade_cliente = criar_text_field('Idade', 200, 80)
    caixa_cpf_cliente = criar_text_field('CPF', 200, 80)
    caixa_endereco_cliente = criar_text_field('Endereço', 410, 80)
    caixa_telefone_cliente = criar_text_field('Telefone', 200, 80)
    caixa_email_cliente = criar_text_field('Email', 410, 80)

    botao_cadastrar = ft.ElevatedButton(
        text='Cadastrar',
        color=texto_padrao(),
        bgcolor=botao_laranja(),
        width=200,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                             text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter',
                                                     weight=ft.FontWeight.BOLD, )),
        height=50,
        on_click=lambda e: cadastro(),
    )
    botao_cancelar = ft.ElevatedButton(
        text='Cancelar',
        color=laranja_aviso(),
        bgcolor=botao_branco(),
        width=200,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                             text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter',
                                                     weight=ft.FontWeight.BOLD, )),
        height=50,
        on_click=lambda e: cancelar_edicao(e),
        visible=False
    )

    botao_editar = ft.ElevatedButton(
        text='Editar',
        color=texto_padrao(),
        bgcolor=botao_laranja(),
        width=200,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10),
                             text_style=ft.TextStyle(color=texto_padrao(), size=16, font_family='Inter',
                                                     weight=ft.FontWeight.BOLD, )),
        height=50,
        on_click=lambda e: editar(e),
        visible=False
    )

    column_left = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(controls=[
                    ft.Container(
                        content=ft.Column(controls=[

                            ft.Container(
                                content=ft.Row(controls=[caixa_pesquisa, botao_pesquisa],
                                               alignment=ft.MainAxisAlignment.START,
                                               spacing=10),
                                width=405,
                                height=50,

                            ),
                            ft.Container(
                                content=ft.Column(controls=[
                                    ft.Row(controls=[caixa_nome_cliente, ]),
                                    ft.Row(controls=[caixa_cpf_cliente]),
                                    ft.Row(controls=[caixa_telefone_cliente, caixa_idade_cliente]),
                                    ft.Row(controls=[caixa_endereco_cliente]),
                                    ft.Row(controls=[caixa_email_cliente]),
                                    ft.Row(controls=[botao_cancelar, botao_cadastrar, botao_editar, ], ),
                                ], alignment=ft.MainAxisAlignment.START, spacing=0),

                            )
                        ], alignment=ft.MainAxisAlignment.START,
                        ),
                        alignment=ft.alignment.center,
                        # bgcolor=fundo_neutro(),
                        padding=ft.padding.all(30),
                        width=page.width / 2,
                    ),
                ]
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            width=page.width,
            height=page.height,
        ),

        alignment=ft.alignment.bottom_left,
    )

    def set_id():
        id = funcoes.quantidade_registros(arquivo_cliente, cliente)
        id += 1
        caixa_id_cliente.value = str(id)

    set_id()

    def cadastro():
        try:
            id = int(caixa_id_cliente.value)
            nome = caixa_nome_cliente.value
            idade = int(caixa_idade_cliente.value)
            cpf = caixa_cpf_cliente.value
            endereco = caixa_endereco_cliente.value
            telefone = caixa_telefone_cliente.value
            email = caixa_email_cliente.value
            cliente.salvar_registro(arquivo_cliente, cliente.criar_registro(id, nome=nome, idade=idade, cpf=cpf,
                                                                            endereco=endereco, telefone=telefone,
                                                                            email=email))
            set_id()
            caixa_nome_cliente.value = ''
            caixa_idade_cliente.value = ''
            caixa_cpf_cliente.value = ''
            caixa_endereco_cliente.value = ''
            caixa_telefone_cliente.value = ''
            caixa_email_cliente.value = ''
            page.add(alert(mensagem="Cliente cadastrado com sucesso", icone="CHECK", cor=fundo_neutro()))
        except:
            page.add(alert(mensagem="Insira todos os dados", icone="ERROR", cor=laranja_aviso()))

        page.update()

    def editar(e):
        caixa_id_cliente.disabled = True
        # caixa_idade_cliente.bgcolor = fundo_neutro()
        # caixa_nome_cliente.bgcolor = fundo_neutro()
        # caixa_cpf_cliente.bgcolor = fundo_neutro()
        # caixa_endereco_cliente.bgcolor = fundo_neutro()
        # caixa_telefone_cliente.bgcolor = fundo_neutro()
        # caixa_email_cliente.bgcolor = fundo_neutro()
        botao_cancelar.visible = True
        caixa_idade_cliente.disabled = False
        caixa_nome_cliente.disabled = False
        caixa_cpf_cliente.disabled = False
        caixa_endereco_cliente.disabled = False
        caixa_telefone_cliente.disabled = False
        caixa_email_cliente.disabled = False
        botao_editar.visible = False
        botao_cadastrar.text = 'Salvar'
        botao_cancelar.text = 'Cancelar'
        botao_cadastrar.visible = True
        botao_cadastrar.on_click = lambda e: salvar_edicao(e)
        e.page.update()

    def busca(e, t_busca, log):
        page.dialog = loading_dialog
        loading_dialog.open = True
        page.update()
        global registro
        try:
            id = int(caixa_pesquisa.value)
            if t_busca == 'Sequencial':
                registro = pesquisa_sequencial(id, arquivo_cliente, cliente, log)
            else:
                registro = pesquisa_binaria(id, arquivo_cliente, cliente, log)
            if registro == -1:
                loading_dialog.open = False
                page.update()
                caixa_nome_cliente.value = ''
                caixa_idade_cliente.value = ''
                caixa_cpf_cliente.value = ''
                caixa_endereco_cliente.value = ''
                caixa_telefone_cliente.value = ''
                caixa_email_cliente.value = ''
                page.add(alert(mensagem="Aluguel Não Encontrado", icone="ERROR"))

            else:
                loading_dialog.open = False
                page.update()
                caixa_id_cliente.disabled = True
                caixa_idade_cliente.disabled = True
                caixa_nome_cliente.disabled = True
                caixa_cpf_cliente.disabled = True
                caixa_endereco_cliente.disabled = True
                caixa_telefone_cliente.disabled = True
                caixa_email_cliente.disabled = True
                botao_editar.visible = True
                botao_cancelar.text = 'Voltar'
                botao_cancelar.on_click = lambda e: cancelar_edicao(e)
                botao_cadastrar.visible = False
                caixa_pesquisa.label = 'Cliente encontrado'
                caixa_id_cliente.value = registro.codigo

                caixa_nome_cliente.value = registro.nome
                caixa_idade_cliente.value = registro.idade
                caixa_cpf_cliente.value = registro.cpf
                caixa_email_cliente.value = registro.email
                caixa_telefone_cliente.value = registro.telefone
                caixa_endereco_cliente.value = registro.endereco

        except ValueError:
            loading_dialog.open = False
            page.update()
            caixa_pesquisa.label = 'Digite um número'
            page.add(alert(mensagem="Digite um numero", icone="ERROR"))
        e.page.update()

    def salvar_edicao(e):
        posicao = arquivo_cliente.tell() - cliente.tamanho_registro()
        arquivo_cliente.seek(posicao)
        nome = caixa_nome_cliente.value
        idade = int(caixa_idade_cliente.value)
        cpf = caixa_cpf_cliente.value
        endereco = caixa_endereco_cliente.value
        telefone = caixa_telefone_cliente.value
        email = caixa_email_cliente.value
        registro = cliente.criar_registro(int(caixa_id_cliente.value), nome=nome, idade=idade, cpf=cpf,
                                          endereco=endereco, telefone=telefone, email=email)
        cliente.salvar_registro(registro=registro, arquivo=arquivo_cliente)
        caixa_idade_cliente.value = ''
        caixa_nome_cliente.value = ''
        caixa_cpf_cliente.value = ''
        caixa_endereco_cliente.value = ''
        caixa_telefone_cliente.value = ''
        caixa_email_cliente.value = ''
        botao_cadastrar.text = 'Cadastrar'
        botao_cadastrar.on_click = lambda e: cadastro()
        botao_cadastrar.visible = True
        botao_cancelar.visible = False
        set_id()
        page.add(alert(mensagem="Cliente editado com sucesso", icone="CHECK", cor=fundo_neutro()))

    def cancelar_edicao(e):
        # caixa_idade_cliente.bgcolor = fundo_neutro()
        # caixa_nome_cliente.bgcolor = fundo_neutro()
        # caixa_cpf_cliente.bgcolor = fundo_neutro()
        # caixa_endereco_cliente.bgcolor = fundo_neutro()
        # caixa_telefone_cliente.bgcolor = fundo_neutro()
        # caixa_email_cliente.bgcolor = fundo_neutro()
        botao_cancelar.visible = False
        caixa_idade_cliente.value = ''
        caixa_nome_cliente.value = ''
        caixa_cpf_cliente.value = ''
        caixa_endereco_cliente.value = ''
        caixa_telefone_cliente.value = ''
        caixa_email_cliente.value = ''
        caixa_idade_cliente.visible = True
        botao_editar.disabled = False
        botao_editar.visible = False
        botao_cadastrar.text = 'Cadastrar'
        botao_cadastrar.on_click = lambda e: cadastro()
        set_id()
        e.page.update()

    return [
        ft.Container(
            ft.Column(
                controls=[
                    column_left
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                width=page.width,

            ),
            padding=ft.padding.all(30),
            alignment=ft.alignment.center,

        )
    ]
