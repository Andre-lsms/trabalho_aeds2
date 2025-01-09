from Entidades.entidade_base import EntidadeBase

import random


class Carro(EntidadeBase):
    @classmethod
    def get_formato(cls):
        # Define o formato do registro para Carro
        return '=i30s30s30s7sH'

    def criar_registro(self, cod, **kwargs):
        codigo = cod
        cor = (self.fake.color_name())[:30]
        placa = (self.fake.numerify(text='###-####'))[:7]
        marca = random.choice(list(marcas_modelos.keys()))
        modelo = random.choice(marcas_modelos[marca])
        ano = self.fake.random_int(min=2018, max=2025)
        return codigo, marca.encode('utf-8'), cor.encode('utf-8'), modelo.encode('utf-8'), placa.encode('utf-8'), ano

    def imprimir_registro(self, arquivo):
        registro_lido = self.ler_registro(arquivo)
        if registro_lido[0] is None:
            return
        print('[CARRO]')
        print(f"Codigo: [{registro_lido[0]}]")
        print(f"Cor: {registro_lido[2].decode('utf-8').rstrip(chr(0))}")
        print(f"Placa: {registro_lido[4].decode('utf-8').rstrip(chr(0))}")
        print(f"Marca: {registro_lido[1].decode('utf-8').rstrip(chr(0))}")
        print(f"Modelo: {registro_lido[3].decode('utf-8').rstrip(chr(0))}")
        print(f"Ano: {registro_lido[5]}")
        print(f'{80 * "-"}')


marcas_modelos = {
    "Toyota": ["Corolla", "Camry", "RAV4"],
    "Volkswagen": ["Golf", "Tiguan", "ID.4"],
    "Ford": ["F-150", "Mustang", "Escape"],
    "Honda": ["Civic", "CR-V", "Accord"],
    "Hyundai": ["Kona EV", "Ioniq 5", "Santa Fe"],
    "Kia": ["Seltos", "EV6", "Sportage"],
    "Chevrolet": ["Silverado", "Bolt EV", "Camaro"],
    "Mercedes-Benz": ["C-Class", "GLE", "EQC"],
    "BMW": ["3 Series", "X5", "iX"],
    "Audi": ["A4", "Q5", "e-tron"],
    "Tesla": ["Model 3", "Model Y", "Model S"],
    "Porsche": ["911", "Taycan", "Macan"],
    "Ferrari": ["SF90 Stradale", "488 Pista", "Roma"],
    "Lamborghini": ["Urus", "Huracán", "Aventador"],
    "Rolls-Royce": ["Phantom", "Ghost", "Spectre"],
    "Aston Martin": ["DBX", "Vantage", "DB11"]
}
