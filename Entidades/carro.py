from Entidades.entidade_base import EntidadeBase

import random


class Carro(EntidadeBase):
    @classmethod
    def get_formato(cls):
        # Define o formato do registro para Carro
        return '=i7s30s30s15sH'

    def criar_registro(self, cod, **kwargs):
        codigo = cod
        placa = kwargs.get('placa'[:7], (self.fake.numerify(text='###-####'))[:7])
        marca = kwargs.get('marca'[:30], random.choice(list(marcas_modelos.keys()))[:30])
        modelo = kwargs.get('modelo'[:30], random.choice(marcas_modelos[marca])[:30])
        cor = kwargs.get('cor'[:15], (random.choice(cores))[:15])
        ano = kwargs.get('ano', self.fake.random_int(min=2015, max=2025))
        return codigo, placa.encode('utf-8'), marca.encode('utf-8'), modelo.encode('utf-8'), cor.encode('utf-8'), ano

    def imprimir_registro(self, registro,saida):
        saida.write(f"Codigo: [{registro[0]}]")
        saida.write(f"Placa: {registro[1].decode('utf-8').rstrip(chr(0))}")
        saida.write(f"Marca: {registro[2].decode('utf-8').rstrip(chr(0))}")
        saida.write(f"Modelo: {registro[3].decode('utf-8').rstrip(chr(0))}")
        saida.write(f"Cor: {registro[4].decode('utf-8').rstrip(chr(0))}")
        saida.write(f"Ano: {registro[5]}")
        saida.write(f'{95 * "_"}')


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
