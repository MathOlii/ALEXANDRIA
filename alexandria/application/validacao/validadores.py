
from abc import ABC, abstractmethod
from typing import Optional

from alexandria.config import TAMANHO_MINIMO_SENHA
from alexandria.domain.valor_obj import (
    Cep,
    Cpf,
    Email,
    Telefone,
    Uf,
    ValorInvalido,
)


class RegraValidacao(ABC):
    @abstractmethod
    def validar(self, dados) -> Optional[str]:
        raise NotImplementedError()


class _RegraValueObject(RegraValidacao):
    

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
        
        erros = []
        for regra in self._regras:
            erro = regra.validar(dados)
            if erro:
                erros.append(erro)
        return erros
