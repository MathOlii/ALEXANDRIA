"""Validacao de dados de cadastro (padrao Strategy + Composite leve).

Cada regra e uma estrategia que sabe validar um campo e devolver uma mensagem
de erro. O ValidadorCadastro agrega varias estrategias e roda todas,
acumulando erros. Adicionar uma nova regra nao altera as existentes (OCP).

As proprias regras se apoiam nos Value Objects do dominio, que ja sabem o
que e um valor valido (DRY) - aqui apenas traduzimos para mensagens amigaveis.
"""
from abc import ABC, abstractmethod

from alexandria.config import TAMANHO_MINIMO_SENHA
from alexandria.domain.value_objects import (
    Cep,
    Cpf,
    Email,
    Telefone,
    Uf,
    ValorInvalido,
)


class RegraValidacao(ABC):
    @abstractmethod
    def validar(self, dados):
        """Retorna mensagem de erro (str) ou None se valido."""


class _RegraValueObject(RegraValidacao):
    """Regra generica baseada em um Value Object que valida no construtor."""

    def __init__(self, campo, tipo, mensagem):
        self._campo = campo
        self._tipo = tipo
        self._mensagem = mensagem

    def validar(self, dados):
        try:
            self._tipo(dados.get(self._campo))
            return None
        except ValorInvalido:
            return self._mensagem


class RegraSenha(RegraValidacao):
    def validar(self, dados):
        senha = dados.get("senha") or ""
        if len(senha) < TAMANHO_MINIMO_SENHA:
            return f"Senha deve ter no minimo {TAMANHO_MINIMO_SENHA} caracteres."
        return None


class RegraObrigatorio(RegraValidacao):
    def __init__(self, campo, rotulo):
        self._campo = campo
        self._rotulo = rotulo

    def validar(self, dados):
        if not (dados.get(self._campo) or "").strip():
            return f"{self._rotulo} e obrigatorio."
        return None


class ValidadorCadastro:
    """Agrega as regras de validacao do cadastro de usuario."""

    def __init__(self):
        self._regras = [
            RegraObrigatorio("nome", "Nome"),
            _RegraValueObject("email", Email, "Email invalido."),
            RegraSenha(),
            _RegraValueObject("telefone", Telefone, "Telefone deve ter 11 digitos."),
            _RegraValueObject("cpf", Cpf, "CPF deve ter 11 digitos."),
            _RegraValueObject("cep", Cep, "CEP deve ter 8 digitos."),
            _RegraValueObject("uf", Uf, "UF invalida."),
        ]

    def validar(self, dados):
        """Retorna lista de mensagens de erro (vazia se tudo valido)."""
        erros = []
        for regra in self._regras:
            erro = regra.validar(dados)
            if erro:
                erros.append(erro)
        return erros
