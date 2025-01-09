import struct


class Funcoes:

    def imprimir(self, arquivo, num_entidade):
        registro_lido = self.ler(arquivo, num_entidade)

        if num_entidade == 1:
            if registro_lido is not None:
                print(f"Codigo: {registro_lido[0]}")
                print(f"Nome: {registro_lido[1].decode('utf-8').rstrip(chr(0))}")
                print(f"Idade: {registro_lido[2]}")
                print(f"CPF: {registro_lido[3].decode('utf-8').rstrip(chr(0))}")
                print(f"Endereco: {registro_lido[4].decode('utf-8').rstrip(chr(0))}")
                print(f"Telefone: {registro_lido[5].decode('utf-8').rstrip(chr(0))}")
                print(f"Email: {registro_lido[6].decode('utf-8').rstrip(chr(0))}")



    @staticmethod
    def ler(arquivo, num_entidade):
        formato_registro = ''
        tamanho_registro = 0

        try:
            if num_entidade == 1:
                formato_registro = '=i30si14s70s15s30s'  # o = é para ter controle total sobre os bytes
                tamanho_registro = struct.calcsize(formato_registro)

            # le os bytes necessarios para um registro completo
            registro_bytes = arquivo.read(tamanho_registro)

            # verifica se o numero de bytes é menor que o esperado
            if len(registro_bytes) < tamanho_registro:
                return None

            # desempacota os campos
            dados = struct.unpack(formato_registro, registro_bytes)

            return dados


        except struct.error as e:
            print(f"Erro ao desempacotar registro: {e}")
            return None
