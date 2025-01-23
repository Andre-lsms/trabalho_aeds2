from Entidades.clientes import Cliente
from Entidades.carro import Carro
from Entidades.filial import Filial

arquivo = open('Bases/cliente.dat', 'w+b')

carro = Filial()
carro.criar_base(10, arquivo=arquivo)
carro.imprimir_base(arquivo)
arquivo.close()