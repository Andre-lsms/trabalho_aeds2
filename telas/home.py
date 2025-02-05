from time import sleep
from Entidades import funcoes
from Funcoes.pesquiesa import *
from telas.templates import *
from Funcoes.alert import alert,loading
cliente_busca = None
carro_busca = None
filial_busca = None
registro = None


def home(page: ft.Page, arquivo_aluguel, aluguel, arquivo_cliente, cliente, arquivo_carro, carro,
         arquivo_filial, filial, arquivo_log, tipo_pesquisa=''):
    page.padding = 0
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
    caixa_id_cliente = criar_text_field('Código', 200, 50, prefix_text='#')
    caixa_nome_cliente = criar_text_field('Nome', 410, 50)
    caixa_idade_cliente = criar_text_field('Idade', 200, 50)
    caixa_cpf_cliente = criar_text_field('CPF', 200, 50)
    caixa_endereco_cliente = criar_text_field('Endereço', 410, 50)
    caixa_telefone_cliente = criar_text_field('Telefone', 200, 50)
    caixa_email_cliente = criar_text_field('Email', 410, 50)
    caixa_id_carro = criar_text_field('Código', 200, 50, prefix_text='#')
    caixa_placa_carro = criar_text_field('Placa', 200, 50)
    caixa_marca_carro = criar_text_field('Marca', 200, 50)
    caixa_modelo_carro = criar_text_field('Modelo', 200, 50)
    caixa_cor_carro = criar_text_field('Cor', 200, 50)
    caixa_ano_carro = criar_text_field('Ano', 200, 50)
    caixa_id_filial = criar_text_field('Código', 200, 50, prefix_text='#')
    caixa_nome_filial = criar_text_field('Nome', 410, 50)
    caixa_endereco_filial = criar_text_field('Endereço', 410, 50)
    caixa_telefone_filial = criar_text_field('Telefone', 200, 50)
    caixa_email_filial = criar_text_field('Email', 410, 50)
    caixa_valor_diaria = criar_text_field('Valor da diária', 200, 50, prefix_text='R$')
    caixa_data_aluguel = criar_text_field('Data do aluguel', 200, 50)
    caixa_tempo = criar_text_field('Tempo', 200, 50)
    caixa_valor_total = criar_text_field('Valor Total', 200, 50, prefix_text='R$')

    botao_devolver = ft.ElevatedButton(
        text='Devolver',
        color=texto_padrao(),
        bgcolor=botao_laranja(),
        width=200,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        height=50,
        on_click=lambda e: devolver(),
        visible=False
    )
    photos_carros = ft.Image(
        src="telas/assets/img/cars/default.png",
        error_content=ft.Text('Erro ao carregar imagem'),
        fit=ft.ImageFit.CONTAIN,
        expand=True,
    )
    row_pesquisa = ft.Container(
        content=ft.Row(
            controls=[caixa_pesquisa, botao_pesquisa],
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        margin=ft.margin.only(bottom=10),
    )
    column_cliente = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Text('DADOS DO LOCATÁRIO', size=14, weight=ft.FontWeight.BOLD,color=laranja_aviso()),
                    bgcolor=principal(),
                    width=410,
                    height=30,
                    border_radius=10,
                    alignment=ft.alignment.center,
                ),
                ft.Row(controls=[caixa_nome_cliente]),
                ft.Row(controls=[caixa_id_cliente,caixa_cpf_cliente]),
                ft.Row(controls=[caixa_telefone_cliente, caixa_idade_cliente]),
                ft.Row(controls=[caixa_email_cliente]),
                ft.Row(controls=[caixa_endereco_cliente]),
            ],
        ),
        border_radius=10,
        padding=ft.padding.all(10),
    )
    column_carro = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text('DADOS DO CARRO', size=14, weight=ft.FontWeight.BOLD,color=laranja_aviso()),
                            bgcolor=principal(),
                            width=410,
                            height=30,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                    ]
                ),
                ft.Row(controls=[caixa_placa_carro, caixa_id_carro]),
                ft.Row(controls=[caixa_marca_carro, caixa_modelo_carro,],),
                ft.Row(controls=[caixa_cor_carro, caixa_ano_carro],),
            ],
        ),
        border_radius=10,
        padding=ft.padding.all(10),
        width=430,
    )
    column_filial = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text('DADOS DA FILIAL', size=14, weight=ft.FontWeight.BOLD,color=laranja_aviso()),
                            bgcolor=principal(),
                            width=410,
                            height=30,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                    ]
                ),
                ft.Row(controls=[caixa_nome_filial]),
                ft.Row(controls=[ caixa_id_filial, caixa_telefone_filial]),
                ft.Row(controls=[caixa_email_filial]),
                ft.Row(controls=[caixa_endereco_filial]),
            ]
        ),
        border_radius=10,
        padding=ft.padding.all(10),
        width=430,
    )
    column_aluguel = ft.Container(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text('DADOS DO ALUGUEL', size=14, weight=ft.FontWeight.BOLD,color=laranja_aviso()),
                            bgcolor=principal(),
                            width=410,
                            height=30,
                            border_radius=10,
                            alignment=ft.alignment.center,
                        ),
                    ],
                    expand=True
                ),
                ft.Row(controls=[caixa_data_aluguel, caixa_tempo]),
                ft.Row(controls=[caixa_valor_diaria, caixa_valor_total]),
                ft.Row(controls=[botao_devolver])
            ],
            expand=True
        ),
        border_radius=10,
        padding=ft.padding.all(10),
        width=430,
    )
    column_info = ft.Container(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Column(
                            controls=[column_cliente,column_filial],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True
                        ),
                    ]
                ),
                ft.Column(
                    controls=[column_carro,column_aluguel],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Column(controls=[ft.Container(content=photos_carros, height=600, width=600, padding=10,
                                                 alignment=ft.alignment.bottom_center)], )
            ],
            spacing=20,
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        ),
    )

    def update_img(nome_carro):
        photos_carros.src = f'telas/assets/img/cars/{nome_carro}.png'
        photos_carros.update()

    def busca(e, t_busca, log):
        global cliente_busca, carro_busca, filial_busca, registro
        page.dialog = loading_dialog
        loading_dialog.open = True
        page.update()
        if caixa_pesquisa.value != '':

            try:
                id = int(caixa_pesquisa.value)
                if t_busca == 'Binaria':
                    registro = pesquisa_binaria(id, arquivo_aluguel, aluguel, arquivo_log)
                    if registro != -1:
                        cliente_busca = funcoes.pesquisa_binaria(registro.cliente.codigo, arquivo_cliente, cliente, log)
                        carro_busca = funcoes.pesquisa_binaria(registro.carro.codigo, arquivo_carro, carro, log)
                        filial_busca = pesquisa_binaria(registro.filial.codigo, arquivo_filial, filial, log)
                else:
                    registro = pesquisa_sequencial(id, arquivo_aluguel, aluguel, arquivo_log)
                    if registro != -1:
                        cliente_busca = pesquisa_sequencial(registro.cliente.codigo, arquivo_cliente, cliente, log)
                        carro_busca = pesquisa_sequencial(registro.carro.codigo, arquivo_carro, carro, log)
                        filial_busca = pesquisa_sequencial(registro.filial.codigo, arquivo_filial, filial, log)

                if registro == -1 or registro.devolvido:
                    loading_dialog.open = False
                    page.update()
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
                    limpar_caixas(caixa_data_aluguel)
                    limpar_caixas(caixa_tempo)
                    limpar_caixas(caixa_valor_total)
                    page.add(alert(mensagem="Aluguel Não Encontrado", icone="ERROR", cor=laranja_aviso()))
                    caixa_pesquisa.label = 'Aluguel não encontrado'
                    limpar_caixas(caixa_pesquisa)
                    caixa_pesquisa.focus()
                    update_img("default")
                else:
                    loading_dialog.open = False
                    page.update()
                    caixa_pesquisa.label = 'Aluguel encontrado'
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

                    # Aluguel
                    caixa_valor_diaria.value = registro.diaria
                    caixa_data_aluguel.value = registro.data_aluguel
                    caixa_tempo.value = registro.tempo
                    caixa_valor_total.value = registro.valor_total
                    botao_devolver.visible = True

                    if carro_busca.modelo != '':
                        update_img(carro_busca.modelo)
                    else:
                        update_img("Default")
                    e.page.update()

            except ValueError:
                loading_dialog.open = False
                page.update()
                page.add(alert(mensagem="Digite um numero", icone="ERROR"))

        e.page.update()

    def devolver():
        global registro, carro_busca
        carro_busca.codigo = int(caixa_id_carro.value)
        aluguel.devolver(arquivo=arquivo_aluguel, registro=registro, arquivo_carro=arquivo_carro, carro=carro_busca)
        page.add(alert(mensagem="Devolução realizada com sucesso", icone=ft.icons.CHECK, cor=texto_padrao()))

    def limpar_caixas(caixa):
        caixa.value = ''

    return [
        ft.Container(
            ft.Column(
                controls=[row_pesquisa, column_info
                          ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                spacing=10,
            ),
            padding=ft.padding.all(0),
            margin=ft.margin.only(left=30),
            expand=True
        )
    ]
