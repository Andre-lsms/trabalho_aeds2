import flet as ft
from telas.colors import *


def alert(mensagem='INSIRA A MENSAGEM DE ERRO', icone='ERROR', cor=laranja_aviso()):
    alerta = ft.AlertDialog(
        icon=ft.Icon(name=icone, color=cor, ),
        title=ft.Text(mensagem, color=cor, size=20, weight=ft.FontWeight.BOLD,
                      text_align=ft.TextAlign.CENTER),
        bgcolor=principal(),
        open=True,
    )
    return alerta


def loading(mensagem="CARREGANDO..."):
    return ft.AlertDialog(
        modal=True,  # Bloqueia interações com a tela principal
        content=ft.Container(
            content=ft.Row(
                controls=[
                    ft.ProgressRing(width=50, height=50, color=laranja_aviso()),
                    ft.Text(mensagem, size=18, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            padding=20,
            width=250,  # Define um tamanho fixo para evitar que fique grande demais
            height=100,  # Mantém compacto
            alignment=ft.alignment.center,
        ),
        bgcolor=principal(),
        shape=ft.RoundedRectangleBorder(radius=15),  # Bordas arredondadas
        open=True,
    )
