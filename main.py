from Entidades.clientes import Cliente
from Entidades.carro import Carro
from Entidades.filial import Filial
from Funcoes.pesquiesa import *

arquivo = open('Bases/cliente.dat', 'w+b')

carro = Cliente()
carro.criar_base(10, arquivo=arquivo)
# pesquisa_sequencial(6,arquivo,carro)
pesquisa_binaria(5,arquivo,carro)
arquivo.close()