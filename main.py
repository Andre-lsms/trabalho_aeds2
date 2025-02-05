from Entidades.clientes import Cliente
from Entidades.carro import Carro
from Entidades.filial import Filial
from Entidades.aluguel import Aluguel
from Funcoes.pesquiesa import *

arquivo_cliente = open('Bases/cliente.dat', 'w+b')
arquivo_carro = open('Bases/carro.dat', 'w+b')
arquivo_filial = open('Bases/filial.dat', 'w+b')
arquivo = open('Bases/aluguel.dat', 'w+b')

clientes = Cliente()
carros = Carro()
filiais = Filial()
alugueis = Aluguel()

clientes.criar_base(10000, arquivo=arquivo_cliente)
carros.criar_base(10000, arquivo=arquivo_carro)
filiais.criar_base(10000, arquivo=arquivo_filial)

alugueis.criar_base(10000, arquivo=arquivo, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                    arquivo_filial=arquivo_filial)


while True:
    print('Bem vindo ao sistema de aluguel de carros')
    print('Escolha uma opção:')
    print('0 - Voltar')
    print('1 - Adicionar ou procurar aluguel')
    print('2 - Adicionar ou procurar cliente')
    print('3 - Imprimir base')
    opcao = int(input('Digite a opção desejada: '))
    if opcao == 1:
        print('Escolha uma opção:')
        print('0 - Voltar')
        print('1 - Adicionar aluguel')
        print('2 - Procurar aluguel')
        opcao_aluguel = int(input('Digite a opção desejada: '))
        if opcao_aluguel == 1:
            nome = input('Digite o nome do cliente: ')
            idade = int(input('Digite a idade do cliente: '))
            cpf = input('Digite o cpf do cliente: ')
            email = input('Digite o email do cliente: ')
            telefone = input('Digite o telefone do cliente: ')
            endereco = input('Digite o endereco do cliente: ')
            cliente = Cliente.criar_registro(codigo=(clientes.quantidade_registros()+1),nome=nome, idade=idade, cpf=cpf, email=email, telefone=telefone, endereco=endereco)
            cliente.salvar_registro(arquivo_cliente, cliente)
            print('Cliente adicionado com sucesso')
        elif opcao_aluguel==2:
            while True:
                print('Escolha uma opção:')
                print('0 - Voltar')
                print('1 - Pesquisa sequencial')
                print('2 - Pesquisa binária')
                opcao_pesquisa = int(input('Digite a opção desejada: '))
                if opcao_pesquisa == 1:
                    id = int(input('Digite o id do aluguel: '))
                    registro = pesquisa_sequencial(id, arquivo, alugueis)
                    if registro == -1:
                        print('Aluguel não encontrado')
                    else:
                        alugueis.imprimir(registro)

                elif opcao_pesquisa == 2:
                    id = input('Digite o id do aluguel: ')
                    registro = pesquisa_binaria(id, arquivo, alugueis)
                    if registro ==-1:
                        print('Aluguel não encontrado')
                    else:
                        alugueis.imprimir(registro)
                elif opcao_pesquisa == 0:
                    break
                else:
                    print('Opção inválida')
    elif opcao == 2:
        print('Escolha uma opção:')

    elif opcao == 3:
        print('Escolha uma opção:')
    elif opcao == 0:
        print('Escolha uma opção:')
        break
    else:
        print('Opção inválida')