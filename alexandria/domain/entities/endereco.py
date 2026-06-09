"""Entidade Endereco (lado "1" do relacionamento 1:1 com Usuario)."""


class Endereco:
    def __init__(self, rua, numero, bairro, cep, cidade, uf,
                 usuario_id=None, id=None):
        self.id = id
        self.rua = rua
        self.numero = numero
        self.bairro = bairro
        self.cep = cep
        self.cidade = cidade
        self.uf = uf
        self.usuario_id = usuario_id

    def __str__(self):
        return (f"{self.rua}, {self.numero} - {self.bairro}, "
                f"{self.cidade}/{self.uf} - CEP: {self.cep}")
