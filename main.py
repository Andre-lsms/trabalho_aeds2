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

clientes.criar_base(100, arquivo=arquivo_cliente)
carros.criar_base(100, arquivo=arquivo_carro)
filiais.criar_base(100, arquivo=arquivo_filial)

alugueis.criar_base(100, arquivo=arquivo, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                    arquivo_filial=arquivo_filial)
alugueis.imprimir_base(arquivo)

