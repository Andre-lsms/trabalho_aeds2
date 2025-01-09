from Entidades.entidade_base import EntidadeBase
from Entidades import funcoes




class Filial(EntidadeBase):
    @classmethod
    def get_formato(cls):
        # Define o formato do registro para Filial
        return '=i30s70s20s30s'

    def criar_registro(self, cod, arquivo):
        codigo = cod
        nome = (self.fake.company())[:30]
        endereco = (funcoes.gerar_endereco())[:70]
        telefone = (self.fake.cellphone_number())[:20]
        email = (self.fake.email())[:30]
        return codigo, nome.encode('utf-8'), endereco.encode('utf-8'), telefone.encode('utf-8'), email.encode('utf-8')

    def imprimir_registro(self, registro):
        registro_lido = self.ler_registro(registro)
        print(f"Codigo: [{registro_lido[0]}]")
        print(f"Nome: {registro_lido[1].decode('utf-8').rstrip(chr(0))}")
        print(f"Endereco: {registro_lido[2].decode('utf-8').rstrip(chr(0))}")
        print(f"Telefone: {registro_lido[3].decode('utf-8').rstrip(chr(0))}")
        print(f"Email: {registro_lido[4].decode('utf-8').rstrip(chr(0))}")
        print(f'{80 * "-"}')
