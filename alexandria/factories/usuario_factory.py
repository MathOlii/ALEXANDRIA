"""Padrao FACTORY para criacao de usuarios.

Concentra a decisao de qual subclasse de Usuario instanciar a partir do
tipo de acesso. O codigo cliente nao precisa conhecer as classes concretas
nem repetir o "if tipo == admin" em varios lugares (OCP/SRP).
"""
from alexandria.domain.entities.usuario import (
    TIPO_ADMIN,
    TIPO_CLIENTE,
    Administrador,
    Cliente,
)

_CRIADORES = {
    TIPO_CLIENTE: Cliente,
    TIPO_ADMIN: Administrador,
}


class UsuarioFactory:
    @staticmethod
    def criar(tipo, nome, email, senha, telefone, cpf, id=None):
        criador = _CRIADORES.get(tipo)
        if criador is None:
            raise ValueError(f"Tipo de usuario desconhecido: {tipo}")
        return criador(nome, email, senha, telefone, cpf, id=id)
