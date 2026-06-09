"""Objetos de Valor (Value Objects).

Calistenia de Objetos: "encapsule todos os tipos primitivos".
Em vez de carregar email/cpf/telefone como strings cruas espalhadas pelo
sistema, criamos pequenos tipos imutaveis que se auto-validam ao nascer.
Se um objeto existe, ele e valido. Isso concentra a regra de formato em um
unico lugar (SRP) e impede estados invalidos.
"""
import re

from alexandria.config import (
    TAMANHO_CEP,
    TAMANHO_CPF,
    TAMANHO_TELEFONE,
    UFS_VALIDAS,
)


class ValorInvalido(ValueError):
    """Erro de dominio levantado quando um value object recebe valor invalido."""


def _somente_digitos(texto):
    return "".join(filter(str.isdigit, texto or ""))


class Email:
    _PADRAO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    def __init__(self, valor):
        valor = (valor or "").strip().lower()
        if not self._PADRAO.match(valor):
            raise ValorInvalido("Email invalido.")
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def __str__(self):
        return self._valor

    def __eq__(self, outro):
        return isinstance(outro, Email) and outro._valor == self._valor

    def __hash__(self):
        return hash(self._valor)


class Cpf:
    def __init__(self, valor):
        digitos = _somente_digitos(valor)
        if len(digitos) != TAMANHO_CPF:
            raise ValorInvalido(f"CPF deve ter {TAMANHO_CPF} digitos.")
        self._digitos = digitos

    @property
    def valor(self):
        return self._digitos

    def formatado(self):
        d = self._digitos
        return f"{d[:3]}.{d[3:6]}.{d[6:9]}-{d[9:]}"

    def __str__(self):
        return self.formatado()


class Telefone:
    def __init__(self, valor):
        digitos = _somente_digitos(valor)
        if len(digitos) != TAMANHO_TELEFONE:
            raise ValorInvalido(f"Telefone deve ter {TAMANHO_TELEFONE} digitos.")
        self._digitos = digitos

    @property
    def valor(self):
        return self._digitos

    def formatado(self):
        d = self._digitos
        return f"({d[:2]}) {d[2]} {d[3:7]}-{d[7:]}"

    def __str__(self):
        return self.formatado()


class Cep:
    def __init__(self, valor):
        digitos = _somente_digitos(valor)
        if len(digitos) != TAMANHO_CEP:
            raise ValorInvalido(f"CEP deve ter {TAMANHO_CEP} digitos.")
        self._digitos = digitos

    @property
    def valor(self):
        return self._digitos

    def formatado(self):
        d = self._digitos
        return f"{d[:5]}-{d[5:]}"

    def __str__(self):
        return self.formatado()


class Uf:
    def __init__(self, valor):
        sigla = (valor or "").strip().upper()
        if sigla not in UFS_VALIDAS:
            raise ValorInvalido("UF invalida.")
        self._sigla = sigla

    @property
    def valor(self):
        return self._sigla

    def __str__(self):
        return self._sigla
