TIPO_CLIENTE = "cliente"
TIPO_ADMIN = "admin"


class Usuario:
    def __init__(self, nome, email, senha, telefone, cpf, tipo_acesso, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.cpf = cpf
        self.tipo_acesso = tipo_acesso

    def eh_admin(self):
        return self.tipo_acesso == TIPO_ADMIN

    def __str__(self):
        return f"[{self.id}] {self.nome} <{self.email}> ({self.tipo_acesso})"


class Cliente(Usuario):
    def __init__(self, nome, email, senha, telefone, cpf, id=None):
        super().__init__(nome, email, senha, telefone, cpf, TIPO_CLIENTE, id)


class Administrador(Usuario):
    def __init__(self, nome, email, senha, telefone, cpf, id=None):
        super().__init__(nome, email, senha, telefone, cpf, TIPO_ADMIN, id)
