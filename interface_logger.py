import sys
import flet as ft

class InterfaceLogger:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        # Enviar para o TextField (interface)
        if message.strip():  # Ignorar linhas vazias
            self.text_widget.value += message + "\n"
            self.text_widget.update()