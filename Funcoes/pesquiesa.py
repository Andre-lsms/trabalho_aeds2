import math
from time import time



def pesquisa_sequencial(id,arquivo,entidade,log):
    quant_arquivos = entidade.quantidade_registros(arquivo)
    arquivo.seek(4)
    t_inicio = time()
    comparacoes = 0
    for i in range(quant_arquivos):
        registro = entidade.ler_registro(arquivo)
        comparacoes += 1
        if registro.codigo == id:
            log.write('\n' +95*"_")
            log.write(f"\nRegistro [{id}]encontrado - [Busca Sequencial =={entidade.nome_classe}==]")
            log.write(f"\ncomparacoes: {comparacoes}")
            log.write(f"\nTempo: {(time() - t_inicio) * 1000:.2f}ms")
            return registro
    log.write(f"Registro [{id}] não encontrado")
    return -1


def pesquisa_binaria(id, arquivo, entidade, log):
    tamanho = entidade.tamanho_arquivo(arquivo)
    quant_arquivos = tamanho // entidade.tamanho_registro()
    t_inicio = time()
    comparacoes = 0
    arquivo.seek(4)
    inicio = 0
    fim = quant_arquivos - 1
    while inicio <= fim:
        meio = (inicio + fim) // 2
        arquivo.seek((meio * entidade.tamanho_registro()))
        registro = entidade.ler_registro(arquivo)
        comparacoes += 1
        if registro.codigo == id:
            log.write('\n' + 95 * "_")
            log.write(f"\nRegistro [{id}] encontrado - [Busca Binária =={entidade.nome_classe}==]")
            log.write(f"\ncomparacoes: {comparacoes}")
            log.write(f"\nTempo: {(time() - t_inicio) * 1000:.2f}ms")
            bigo = math.ceil(math.log2(quant_arquivos))
            log.write(f'\nPior caso: {bigo}')
            return registro
        elif registro.codigo < id:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1
