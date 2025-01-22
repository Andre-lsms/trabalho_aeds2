import sys

from Entidades.entidade_base import EntidadeBase
from Entidades import funcoes


class Cliente(EntidadeBase):
    @classmethod
    def get_formato(cls):
        # Define o formato do registro para Cliente
        return '=i30si14s70s20s30s'

    def criar_registro(self, cod, **kwargs,):
        codigo = cod
        nome = kwargs.get('nome'[:30], (self.fake.name())[:30])
        idade = kwargs.get('idade', self.fake.random_int(min=18, max=70))
        cpf = kwargs.get('cpf'[:14], self.fake.numerify(text='###.###.###-##'))[:14]
        endereco = kwargs.get('endereco'[:70], self.fake.address()[:70])
        telefone = kwargs.get('telefone'[:20], self.fake.phone_number()[:20])
        email = kwargs.get('email'[:30], self.fake.email()[:30])
        return codigo, nome.encode('utf-8'), idade, cpf.encode('utf-8'), endereco.encode('utf-8'), telefone.encode(
            'utf-8'), email.encode('utf-8')

    def imprimir_registro(self, registro,saida):
        print(f"Codigo: [{registro[0]}]")
        # print(f"Nome: {registro[1].decode('utf-8').rstrip(chr(0))}")
        # print(f"Idade: {registro[2]}")
        # print(f"CPF: {registro[3].decode('utf-8').rstrip(chr(0))}")
        # print(f"Endereco: {registro[4].decode('utf-8', errors='ignore').rstrip(chr(0))}")
        # print(f"Telefone: {registro[5].decode('utf-8').rstrip(chr(0))}")
        # print(f"Email: {registro[6].decode('utf-8').rstrip(chr(0))}")
        # print(f'{95 * "_"}')


