from Entidades.entidade_base import EntidadeBase
from Entidades import funcoes


class Filial(EntidadeBase):
    @classmethod
    def get_formato(cls):
        # Define o formato do registro para Filial
        return '=i30s70s20s30s'

    def criar_registro(self, cod, **kwargs):
        codigo = cod
        nome = kwargs.get('nome'[:30], (self.fake.company())[:30])
        endereco = kwargs.get('endereco'[:70], (funcoes.gerar_endereco())[:70])
        telefone = kwargs.get('telefone'[:20], (self.fake.cellphone_number())[:20])
        email = kwargs.get('email'[:30], (self.fake.email())[:30])

        return codigo, nome.encode('utf-8'), endereco.encode('utf-8'), telefone.encode('utf-8'), email.encode('utf-8')

    def imprimir_registro(self, registro,saida):
        saida.write(f"Codigo: [{registro[0]}]")
        saida.write(f"Nome: {registro[1].decode('utf-8').rstrip(chr(0))}")
        saida.write(f"Endereco: {registro[2].decode('utf-8').rstrip(chr(0))}")
        saida.write(f"Telefone: {registro[3].decode('utf-8').rstrip(chr(0))}")
        saida.write(f"Email: {registro[4].decode('utf-8').rstrip(chr(0))}")
        saida.write(f'{95 * "_"}')

