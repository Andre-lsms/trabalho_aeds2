import os

from Entidades.tabela_hash import Tabela_hash
from Entidades.aluguel import Aluguel
from Entidades.carro import Carro
from Entidades.clientes import Cliente
from Entidades.filial import Filial



arquivo_hash = open('Bases/tabela.dat', 'w+b')
arquivo_cliente = open('Bases/Cliente.dat', f'w+b')
arquivo_carro = open('Bases/Carro.dat', 'w+b')
arquivo_filial = open('Bases/Filial.dat', 'w+b')
arquivo = open('Bases/Aluguel.dat', 'w+b')
arquivo_log = open('Bases/Log2.txt', 'a+')

tam =10
clientes = Cliente()
carros = Carro()
filiais = Filial()
alugueis = Aluguel()
tabela_hash = Tabela_hash(23,arquivo_hash,arquivo)
# m = tam//10
clientes.criar_base(tam, arquivo=arquivo_cliente)
carros.criar_base(tam, arquivo=arquivo_carro)
filiais.criar_base(tam, arquivo=arquivo_filial)

alugueis.criar_base(tam, arquivo=arquivo, arquivo_cliente=arquivo_cliente, arquivo_carro=arquivo_carro,
                    arquivo_filial=arquivo_filial,tabela_hash=tabela_hash)

tabela_hash.exclusao(1)
# # tabela_hash.busca(3)
reg = alugueis.criar_registro(codigo=212,tempo=1,arquivo_cliente=arquivo_cliente,arquivo_carro=arquivo_carro,arquivo_filial=arquivo_filial)
tabela_hash.insercao(reg)
# tabela_hash.busca(1234)
tabela_hash.imprimir_tabela()
alugueis.imprimir_codigos(arquivo)
