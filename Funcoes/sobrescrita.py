def sobrescrever(arquivo, registro):
    posicao = arquivo.tell()
    tamanho_registro = registro.tamanho_registro()
    arquivo.seek(posicao - tamanho_registro)
    registro.salvar_registro(arquivo, registro)
