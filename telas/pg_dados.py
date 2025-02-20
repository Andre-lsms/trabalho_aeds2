import flet as ft

from Funcoes.interface_logger import InterfaceLogger
from telas.colors import *
from Funcoes.config import config
from Funcoes.alert import alert,loading

def data_page(page: ft.Page, arquivo_aluguel, aluguel, arquivo_cliente, cliente, arquivo_carro, carro,
              arquivo_filial, filial, arquivo_log,):
    loading_dialog = loading()
    page.dialog = loading_dialog
    loading_dialog.open = False
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color=ft.colors.TRANSPARENT,  # Apenas a cor direta, sem chaves

            track_visibility=True,
            thumb_visibility=True,
            thumb_color=fundo_neutro(),
            thickness=10,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )


    nome_log = ft.Text(
        size=20,
        weight=ft.FontWeight.BOLD,
        color=texto_padrao(),
    )
    log_box = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
        width=660,
        height=600,
        # auto_scroll=True,
        cache_extent=1000,

    )

    interface_logger = InterfaceLogger(log_box)

    button_log = ft.ElevatedButton(
        text="Log",
        color=laranja_aviso(),
        bgcolor=botao_branco(),
        width=300,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=60,
        on_click=lambda e: open_log(),
    )
    button_ordenar = ft.ElevatedButton(
        text="Ordenar arquivos",
        color=laranja_aviso(),
        bgcolor=botao_branco(),
        width=300,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=60,
        on_click=lambda e: ordenar_bases()
    )
    button_desordenar = ft.ElevatedButton(
        text="Desordenar arquivos",
        color=laranja_aviso(),
        bgcolor=botao_branco(),
        width=300,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=60,
        on_click=lambda e: desordenar_bases(),
    )

    button_imprimir = ft.ElevatedButton(
        text="Imprimir",
        color=texto_padrao(),
        bgcolor=botao_laranja(),
        width=150,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=50,
        on_click=lambda e: imprimir_base(),
    )
    selection = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Alugueis", label="Alugueis", active_color=laranja_aviso(),
                     label_style=ft.TextStyle(color=texto_padrao(), weight=ft.FontWeight.BOLD)),
            ft.Radio(value="Clientes", label="Clientes", active_color=laranja_aviso(),
                     label_style=ft.TextStyle(color=texto_padrao(), weight=ft.FontWeight.BOLD)),
            ft.Radio(value="Carros", label="Carros", active_color=laranja_aviso(),
                     label_style=ft.TextStyle(color=texto_padrao(), weight=ft.FontWeight.BOLD)),
            ft.Radio(value="Filiais", label="Filiais", active_color=laranja_aviso(),
                     label_style=ft.TextStyle(color=texto_padrao(), weight=ft.FontWeight.BOLD, )),

        ],
        )
    )
    clientes_text = ft.Text(f"Clientes: {0}", size=16, weight=ft.FontWeight.BOLD, color=texto_padrao())
    carros_text = ft.Text(f"Carros: {0}", size=16, weight=ft.FontWeight.BOLD, color=texto_padrao())
    filiais_text = ft.Text(f"Filiais: {0}", size=16, weight=ft.FontWeight.BOLD, color=texto_padrao())
    alugueis_text = ft.Text(f"Alugueis: {0}", size=16, weight=ft.FontWeight.BOLD, color=texto_padrao())

    column_left = ft.Column(
        controls=[
            ft.Row(controls=[selection, button_imprimir, ]),
            button_log, button_ordenar, button_desordenar
        ],

        alignment=ft.MainAxisAlignment.START,  # Centraliza o conteúdo no eixo vertical do Column
        horizontal_alignment=ft.CrossAxisAlignment.START,  # Centraliza o conteúdo no eixo horizontal do Column
    )
    column_center = ft.Column(
    )
    column_right = ft.Column(
        controls=[
            ft.Container(
                ft.Column(
                    controls=[
                        ft.Container(
                            content=nome_log,
                            bgcolor=laranja_aviso(),
                            width=300,
                            height=30,  # Define a altura para ver o alinhamento
                            alignment=ft.alignment.center,  # Centraliza o conteúdo no Container
                            margin=ft.margin.only(top=10),
                            border_radius=30
                        ),
                        ft.Container(
                            content=log_box,
                            width=600,
                            bgcolor=principal(),
                        ),
                        ft.Container(
                            ft.Row(

                                controls=[clientes_text, carros_text, filiais_text, alugueis_text],
                                alignment=ft.MainAxisAlignment.END,
                                spacing=20,
                            ),
                            padding=10,
                            height=50,
                            bgcolor=laranja_aviso(),
                            border_radius=ft.border_radius.only(top_left=30, top_right=30),
                        )


                    ],
                    spacing=0,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=principal(),
                border_radius=30,
            )
        ],
        alignment=ft.MainAxisAlignment.START,  # Centraliza o conteúdo no eixo vertical do Column
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )



    def update_data():
        num_clientes = cliente.quantidade_registros(arquivo_cliente)
        num_carros = carro.quantidade_registros(arquivo_carro)
        num_filiais = filial.quantidade_registros(arquivo_filial)
        num_alugueis = aluguel.quantidade_registros(arquivo_aluguel)
        clientes_text.value = f"Clientes: {num_clientes}"
        carros_text.value = f"Carros: {num_carros}"
        filiais_text.value = f"Filiais: {num_filiais}"
        alugueis_text.value = f"Alugueis: {num_alugueis}"
        # Atualiza a interface gráfica
        page.update()
    update_data()

    def open_log():
        page.update()
        nome_log.value = "LOG"

        log_box.controls.clear()
        nome_log.update()  # Atualiza o nome imediatamente
        log_box.update()  # Atualiza a interface do log_box

        try:
            button_log.disabled = True  # Evita cliques múltiplos
            arquivo_log.seek(0)
            log = arquivo_log.read()

            if not log.strip():
                page.add(alert(mensagem="O arquivo de log está vazio!", icone="error", cor=laranja_aviso()))
            else:
                log_box.controls.append(ft.Text(log))  # Exibe os logs
        except Exception as e:
            page.add(alert(mensagem=f"Erro ao abrir log: {str(e)}", icone="error", cor=laranja_aviso()))

        button_log.disabled = False
        log_box.update()
        page.update()

    def desordenar_bases():
        loading_dialog.open = True
        page.update()
        button_desordenar.disabled = True
        config.dados_ordenados = False
        cliente.desordenar_base(arquivo_cliente)
        carro.desordenar_base(arquivo_carro)
        filial.desordenar_base(arquivo_filial)
        aluguel.desordenar_base(arquivo_aluguel)
        log_box.controls.clear()
        log_box.update()
        loading_dialog.open = False
        page.update()
        page.add(alert(mensagem=f"Bases desordenadas", icone="done", cor=laranja_aviso()))
        button_ordenar.disabled = False

    def ordenar_bases():
        loading_dialog.open = True
        page.update()
        button_ordenar.disabled = True
        config.dados_ordenados = True
        cliente.ordenar_base(arquivo_cliente)
        carro.ordenar_base(arquivo_carro)
        filial.ordenar_base(arquivo_filial)
        aluguel.ordenar_base(arquivo_aluguel)
        log_box.controls.clear()
        loading_dialog.open = False
        log_box.update()
        page.update()
        page.add(alert(mensagem=f"Bases ordenadas", icone="done", cor=laranja_aviso()))
        button_desordenar.disabled = False

    def imprimir_base():
        page.dialog.open = True
        page.update()
        global entidade, arquivo
        if selection.value == "Alugueis":
            nome_log.value = "Alugueis"
            entidade = aluguel
            arquivo = arquivo_aluguel
        elif selection.value == "Clientes":
            nome_log.value = "Clientes"
            entidade = cliente
            arquivo = arquivo_cliente
        elif selection.value == "Carros":
            nome_log.value = "Carros"
            entidade = carro
            arquivo = arquivo_carro
        elif selection.value == "Filiais":
            nome_log.value = "Filiais"
            entidade = filial
            arquivo = arquivo_filial
        log_box.controls.clear()
        log_box.update()
        nome_log.update()
        # try:
        button_imprimir.disabled = True
        entidade.imprimir_base(arquivo, interface_logger,)
        # except Exception as e:
        # page.add(alert(mensagem=f"Erro ao imprimir base: {str(e)}", icone="error", cor=laranja_aviso()))
        # page.add(alert(mensagem=f"Escolha uma opção", icone="error", cor=laranja_aviso()))

        button_imprimir.disabled = False
        page.dialog.open = False
        log_box.update()
        page.update()

    return [
        ft.Container(
            ft.Column(
                controls=[ft.Row(
                    controls=[
                        column_left,
                        column_center,
                        column_right
                    ],
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.START,

                ),

                ],
            ),
            padding=ft.padding.Padding(left=30, right=30, top=0, bottom=30),
            alignment=ft.alignment.top_center,
        )
    ]
