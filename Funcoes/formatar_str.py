import random
import re
import random

def formatar_cpf(e):
    texto = ''.join(filter(str.isdigit, e.control.value))
    texto = texto[:11]
    # Aplica a formatação de CPF
    if len(texto) > 9:
        texto_formatado = f"{texto[:3]}.{texto[3:6]}.{texto[6:9]}-{texto[9:]}"
    elif len(texto) > 6:
        texto_formatado = f"{texto[:3]}.{texto[3:6]}.{texto[6:]}"
    elif len(texto) > 3:
        texto_formatado = f"{texto[:3]}.{texto[3:]}"
    else:
        texto_formatado = texto

    # Atualiza o valor do campo com o texto formatado
    e.control.value = texto_formatado
    e.control.update()


def validar_email(e):
    padrao_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    email_valido = re.match(padrao_email, e.control.value)

    if email_valido and e.control.error_text:
        e.control.error_text = ""  # Limpa o erro só se for necessário
        e.control.update()
    elif not email_valido and not e.control.error_text:
        e.control.error_text = "E-mail inválido!"
        e.control.update()

def formatar_telefone(e):
    texto = ''.join(filter(str.isdigit, e.control.value))  # Remove caracteres não numéricos
    texto = texto[:11]  # Limita a 11 dígitos (DDD + Número)

    # Aplica a formatação de telefone
    if len(texto) > 9:  # Celular: (XX) XXXXX-XXXX
        texto_formatado = f"({texto[:2]}) {texto[2:7]}-{texto[7:]}"
    elif len(texto) > 6:  # Telefone fixo: (XX) XXXX-XXXX
        texto_formatado = f"({texto[:2]}) {texto[2:6]}-{texto[6:]}"
    elif len(texto) > 2:  # Apenas DDD preenchido
        texto_formatado = f"({texto[:2]}) {texto[2:]}"
    else:
        texto_formatado = texto  # Apenas os primeiros números digitados

    # Atualiza o valor do campo somente se houver mudança
    if e.control.value != texto_formatado:
        e.control.value = texto_formatado
        e.control.update()  # Atualiza o controle de forma eficiente sem travar
