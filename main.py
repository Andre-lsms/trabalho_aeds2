import struct

import Funcoes.pesquiesa
from Entidades.clientes import Cliente
from Entidades.carro import Carro
from Entidades.filial import Filial
from Entidades.aluguel import Aluguel
from Funcoes.pesquiesa import *

arquivo_cliente = open('Bases/cliente.dat', 'w+b')
arquivo_carro = open('Bases/carro.dat', 'w+b')
arquivo_filial = open('Bases/filial.dat', 'w+b')
arquivo = open('Bases/aluguel.dat', 'w+b')
arquivo_cliente.seek(0)
arquivo_carro.seek(0)
arquivo_filial.seek(0)
arquivo.seek(0)
arquivo.write(struct.pack('i', -1))
arquivo_cliente.write(struct.pack('i', -1))
arquivo_carro.write(struct.pack('i', -1))
arquivo_filial.write(struct.pack('i', -1))

clientes = Cliente()
carros = Carro()
filiais = Filial()
alugueis = Aluguel()
tam = 5
clientes.criar_base(tam, arquivo=arquivo_cliente)
carros.criar_base(12, arquivo=arquivo_carro)
filiais.criar_base(tam, arquivo=arquivo_filial)

alugueis.criar_base(tam, arquivo=arquivo, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                    arquivo_filial=arquivo_filial,desordenada=False)
#
reg1 = Funcoes.pesquiesa.pesquisa_sequencial(1, arquivo, alugueis)
alugueis.excluir_registro(arquivo,reg1)
reg2 = Funcoes.pesquiesa.pesquisa_sequencial(3, arquivo, alugueis)
alugueis.excluir_registro(arquivo,reg2)


#
#
#
alugu = alugueis.criar_registro(123, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro, arquivo_filial=arquivo_filial)
alugueis.salvar_registro(arquivo, alugu)
alugu2 = alugueis.criar_registro(124, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro, arquivo_filial=arquivo_filial)
alugueis.salvar_registro(arquivo, alugu2)
alugueis.imprimir_base(arquivo)

