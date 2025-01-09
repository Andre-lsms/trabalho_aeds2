import struct

from faker import Faker

fake = Faker('pt_BR')


class Cliente:
    def criarar_cliente(self, cod):
        codigo = cod
        nome = (fake.name())[:30]
        idade = fake.random_int(min=18, max=70)
        cpf = (fake.numerify(text='###.###.###-##'))[:14]
        endereco = (self.gerar_endereco())[:70]
        telefone = (fake.phone_number())[:15]
        email = (fake.email())[:30]

        return codigo, nome, idade, cpf, endereco, telefone, email


    def salvar_cliente(self, arquivo, cod):
        cliente = self.criarar_cliente(cod)
        arquivo.write(struct.pack('i', cliente[0]))
        arquivo.write(struct.pack(f'30s', cliente[1].encode('utf-8')))
        arquivo.write(struct.pack('i', cliente[2]))
        arquivo.write(struct.pack('14s', cliente[3].encode('utf-8')))
        arquivo.write(struct.pack('70s', cliente[4].encode('utf-8')))
        arquivo.write(struct.pack('15s', cliente[5].encode('utf-8')))
        arquivo.write(struct.pack('30s', cliente[6].encode('utf-8')))



    @staticmethod
    def gerar_endereco():
        rua = fake.street_name()
        numero = fake.building_number()
        bairro = fake.bairro()
        cidade = fake.city()
        return rua + ', ' + numero + ' - ' + bairro + '. ' + cidade
