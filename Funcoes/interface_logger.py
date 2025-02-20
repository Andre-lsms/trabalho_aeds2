import sys
import flet as ft
import telas.colors


class InterfaceLogger:
    def __init__(self, text_widget, max_linhas=5000, buffer_size=1):
        self.text_widget = text_widget  # ListView ou similar
        self.historico = []  # Armazena todas as mensagens
        self.buffer = []  # Buffer para atualizações em lote
        self.i = 0
        self.max_linhas = max_linhas  # Limite de exibição (sem apagar do histórico)
        self.buffer_size = buffer_size  # Número de mensagens antes de atualizar

    def write(self, message, color=telas.colors.texto_padrao(), buffer=1):
        self.buffer_size = buffer
        if message.strip():
            # Armazena no histórico completo
            self.historico.append(
                ft.Text(message, color=color, size=12, font_family="Inter", weight=ft.FontWeight.BOLD)
            )
            self.historico.append(ft.Divider(color=telas.colors.laranja_aviso(), height=5))

            # Adiciona ao buffer
            self.buffer.append(self.historico[-2])  # Mensagem
            self.buffer.append(self.historico[-1])  # Divider
            self.i += 1

            if self.i >= self.buffer_size:  # Atualiza em lotes
                self.flush()

    def flush(self):
        """Força a atualização do ListView sem perder mensagens antigas."""
        if not self.buffer:
            return

        # Adiciona as novas mensagens
        self.text_widget.controls.extend(self.buffer)
        self.buffer.clear()
        self.i = 0  # Reinicia o contador

        # Mantém um limite no ListView sem perder o histórico
        excesso = len(self.text_widget.controls) - self.max_linhas
        if excesso > 0:
            self.text_widget.controls = self.text_widget.controls[excesso:]  # Remove do ListView, mas mantém no histórico

        self.text_widget.update()

