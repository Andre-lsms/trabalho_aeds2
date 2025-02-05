from telas.colors import *
import flet as ft


def criar_text_field(label, width, height, prefix_text='', disabled=True,align=ft.TextAlign.CENTER,
                     bgcolor=ft.colors.TRANSPARENT):
    return ft.TextField(
        label=f'{label}: ' if not prefix_text else label,
        label_style=ft.TextStyle(
            color=texto_padrao(), size=14, font_family='Inter', weight=ft.FontWeight.BOLD
        ),
        text_style=ft.TextStyle(
            color=texto_padrao(), size=16, font_family='Inter', weight=ft.FontWeight.NORMAL
        ),
        text_align=align,
        bgcolor=bgcolor,
        width=width,
        height=height,
        border=ft.InputBorder.UNDERLINE,
        disabled=disabled,
        content_padding=5,
        expand=True,
        prefix_style=ft.TextStyle( size=14, weight=ft.FontWeight.BOLD),
        prefix=ft.Text(f'{prefix_text}  '),

    )
