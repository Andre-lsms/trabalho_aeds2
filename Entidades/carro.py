import struct

from Entidades.entidade_base import EntidadeBase

import random


class Carro(EntidadeBase):
    def __init__(self, codigo=0, placa=None, marca=None, modelo=None, cor=None, ano=0, disponivel=None):
        super().__init__()
        self.nome_classe = 'Carro'
        self.codigo = codigo
        self.placa = placa
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.ano = ano
        self.disponivel = disponivel

    def criar_registro(self, codigo=0, **kwargs):
        self.codigo = codigo
        self.placa = kwargs.get('placa'[:7], (self.fake.numerify(text='###-####'))[:7])
        self.marca = kwargs.get('marca'[:30], random.choice(list(marcas_modelos.keys()))[:30])
        self.modelo = kwargs.get('modelo'[:30], random.choice(marcas_modelos[self.marca])[:30])
        self.cor = kwargs.get('cor'[:15], (random.choice(cores))[:15])
        self.ano = kwargs.get('ano', self.fake.random_int(min=2015, max=2025))
        self.disponivel = kwargs.get('disponivel', True)
        return Carro(
            codigo=codigo,
            placa=self.placa,
            marca=self.marca,
            modelo=self.modelo,
            cor=self.cor,
            ano=self.ano,
            disponivel=self.disponivel
        )

    def salvar_registro(self, arquivo, registro):
        try:
            arquivo.write(struct.pack('i', registro.codigo))
            arquivo.write(struct.pack('7s', registro.placa.encode('utf-8')))
            arquivo.write(struct.pack('30s', registro.marca.encode('utf-8')))
            arquivo.write(struct.pack('30s', registro.modelo.encode('utf-8')))
            arquivo.write(struct.pack('15s', registro.cor.encode('utf-8')))
            arquivo.write(struct.pack('i', registro.ano))
            arquivo.write(struct.pack('?', registro.disponivel))

        except struct.error as e:
            print(f"Erro ao empacotar registro: {e}")

    def imprimir(self, registro):

        return (f"Código: {registro.codigo}\n"
                  f"Placa: {registro.placa.strip()}\n"
                  f"Marca: {registro.marca.strip()}\n"
                  f"Modelo: {registro.modelo.strip()}\n"
                  f"Cor: {registro.cor.strip()}\n"
                  f"Ano: {registro.ano}\n"
                  f"Disponível: {'Disponível' if registro.disponivel else 'Não disponível'}\n")

    def ler_registro(self, arquivo):
        try:
            registro_bytes = arquivo.read(self.tamanho_registro())
            if len(registro_bytes) < self.tamanho_registro():
                return None

            registro = struct.unpack(self.get_formato(), registro_bytes)
            codigo, placa, marca, modelo, cor, ano, disponivel = registro
            return Carro(
                codigo=codigo,
                placa=placa.decode('utf-8', errors='ignore').rstrip(chr(0)),
                marca=marca.decode('utf-8', errors='ignore').rstrip(chr(0)),
                modelo=modelo.decode('utf-8', errors='ignore').rstrip(chr(0)),
                cor=cor.decode('utf-8', errors='ignore').rstrip(chr(0)),
                ano=ano,
                disponivel=disponivel
            )
        except struct.error as e:
            print(f"Erro ao desempacotar registro: {e}")

    def get_formato(self):
        return '=i7s30s30s15si?'

    def tamanho_registro(self):
        return int(struct.calcsize(self.get_formato()))

    def exibir_disponiveis(self, arquivo, saida):
        arquivo.seek(4)
        while registro_lido := self.ler_registro(arquivo):
            if registro_lido is not None and registro_lido.disponivel:
                saida.write(f"[{registro_lido.codigo}]  {registro_lido.marca} - {registro_lido.modelo},{registro_lido.cor}, {registro_lido.ano}")

marcas_modelos = {
    "Toyota": ["Corolla", "Hilux", "Yaris"],
    "Volkswagen": ["Gol", "Polo", "T-Cross"],
    "Chevrolet": ["Onix", "Tracker", "S10"],
    "Fiat": ["Strada", "Toro", "Argo"],
    "Hyundai": ["HB20", "Creta", "Tucson"],
    "Honda": ["Civic", "HR-V", "City"],
    "Jeep": ["Renegade", "Compass", "Commander"],
    "Renault": ["Sandero", "Duster", "Kwid"],
    "Ford": ["EcoSport", "Ka", "Ranger"],
    "Audi": ["A3", "Q3", "Q5"],
    "BMW": ["320i", "X1", "X5"],
    "Mercedes-Benz": ["C-Class", "GLC", "GLA"],
}

cores = [
    "Preto",
    "Branco",
    "Prata",
    "Cinza",
    "Vermelho",
    "Azul",
    "Verde",
    "Amarelo",
    "Marrom",
    "Dourado",
    "Laranja",
    "Bege",
    "Roxo",
    "Rosa",
    "Bordô",
    "Champanhe",
    "Grafite",
    "Azul Marinho",
    "Verde Limão",
    "Cobre"
]
