import math
import struct

from faker import Faker

fake = Faker('pt_BR')


def escolher_registro(arquivo, entidade, posicao=None):
    quantidade = (tamanho_arquivo(arquivo) // tamanho_registro(entidade))
    if posicao is None:
        posicao = fake.random_int(min=0, max=quantidade - 1)
    arquivo.seek((posicao * tamanho_registro(entidade)))
    registro_lido = entidade.ler_registro(arquivo)
    return registro_lido


def gerar_endereco():
    rua = fake.street_name()
    numero = fake.building_number()
    bairro = fake.bairro()
    cidade = fake.city()
    return rua + ', ' + numero + ' - ' + bairro + '. ' + cidade


def tamanho_arquivo(arquivo):
    arquivo.seek(0, 2)
    return arquivo.tell()


def tamanho_registro(entidade):
    return struct.calcsize(entidade.get_formato())


def pesquisa_sequencial(id, arquivo, endidade):
    tamanho = tamanho_arquivo(arquivo)
    arquivo.seek(0)
    for i in range(tamanho // tamanho_registro(endidade)):
        registro = endidade.ler_registro(arquivo)
        if registro[0] == id:
            print(f"Registro [{id}]encontrado")
            endidade.imprimir_registro(registro)
            return i
    return -1


def pesquisa_binaria(id, arquivo, entidade):
    tamanho = tamanho_arquivo(arquivo)
    total_registros = tamanho // tamanho_registro(entidade)
    inicio = 0
    fim = total_registros - 1
    comparacoes = 0
    arquivo.seek(0)
    while inicio <= fim:
        meio = (inicio + fim) // 2
        arquivo.seek(meio * tamanho_registro(entidade))
        registro = entidade.ler_registro(arquivo)
        comparacoes += 1
        if registro[0] == id:
            print(f"Registro [{id}] encontrado")
            print(f"comparacoes: {comparacoes}")
            bigo = math.ceil(math.log2(total_registros))
            print(f'{bigo}')
            entidade.imprimir_registro(registro)
            return meio
        elif registro[0] < id:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1


'''
 tamanho_registro = Funcionario.tamanhoRegistro()

        # Determinar o número total de registros
        arquivo.seek(0, 2)  # Ir para o final do arquivo
        total_registros = arquivo.tell() // tamanho_registro

        inicio = 0
        fim = total_registros - 1
        comparacoes = 0
        tincio = time()
        arquivo.seek(0)

        while inicio <= fim:
            comparacoes += 1
            meio = (inicio + fim) // 2

            # Posicionar o cursor no início do registro do meio
            arquivo.seek(meio * tamanho_registro)

            # Ler o registro no meio
            funcLido = Funcionario.leFunc(arquivo)

            if funcLido.cod == chave:
                # Registro encontrado
                arquivo.seek(meio * tamanho_registro)

                print(f'Funcionário de código {chave} encontrado!')

                # Registrar os dados em um arquivo de texto
                with open(arquivo_log, 'a') as file:
                    file.write('\n***********************BUSCA BINÁRIA***********************')
                    file.write(f'\nFuncionário de código: {funcLido.cod}')
                    file.write(f'\nNome: {funcLido.nome.decode("utf-8").strip()}')
                    file.write(f'\nCPF: {funcLido.cpf.decode("utf-8").strip()}')
                    file.write(f'\nData de Nascimento: {funcLido.dataNascimento.decode("utf-8").strip()}')
                    file.write(f'\nSalário: {funcLido.salario}')
                    file.write('\n**********************************************')
                    file.write(f'\nNúmero de comparacoes: {comparacoes}')
                    file.write(f'\nTempo de execução: {(time() - tincio) * 1000:.2f} ms\n')
                    file.write('\n**********************************************')


                return True

            elif funcLido.cod < chave:
                # Continuar na metade superior
                inicio = meio + 1
            else:
                # Continuar na metade inferior
                fim = meio - 1

        # Registro não encontrado
        print(f'Funcionário de código {chave} não encontrado.')
        with open(arquivo_log, 'a') as file:
            file.write('\n***********************BUSCA BINÁRIA***********************')
            file.write(f'\nFuncionário de código {chave} não encontrado.')
            file.write(f'\nNúmero de comparacoes: {comparacoes}')
            file.write(f'\nTempo de execução: {(time() - tincio) * 1000:.2f} ms\n')
        return False
'''
