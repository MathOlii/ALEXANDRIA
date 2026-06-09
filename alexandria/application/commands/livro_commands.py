"""Padrao COMMAND para as operacoes de CRUD de livro do administrador.

Cada operacao (inserir, atualizar, deletar) e encapsulada como um objeto
Comando com `executar()` e `desfazer()`. Um Invoker mantem o historico e
permite desfazer a ultima acao - util, por exemplo, para reverter uma
exclusao acidental de livro. Isso desacopla a UI (que so dispara comandos)
da regra de execucao.
"""
from abc import ABC, abstractmethod


class Comando(ABC):
    @abstractmethod
    def executar(self):
        ...

    @abstractmethod
    def desfazer(self):
        ...

    @abstractmethod
    def descricao(self):
        ...


class InserirLivroCommand(Comando):
    def __init__(self, repo, livro):
        self._repo = repo
        self._livro = livro

    def executar(self):
        self._repo.inserir(self._livro)

    def desfazer(self):
        if self._livro.id is not None:
            self._repo.deletar(self._livro.id)

    def descricao(self):
        return f"Inserir livro '{self._livro.titulo}'"


class AtualizarLivroCommand(Comando):
    def __init__(self, repo, livro):
        self._repo = repo
        self._livro = livro
        self._estado_anterior = None

    def executar(self):
        self._estado_anterior = self._repo.buscar_por_id(self._livro.id)
        self._repo.atualizar(self._livro)

    def desfazer(self):
        if self._estado_anterior is not None:
            self._repo.atualizar(self._estado_anterior)

    def descricao(self):
        return f"Atualizar livro #{self._livro.id}"


class DeletarLivroCommand(Comando):
    def __init__(self, repo, livro_id):
        self._repo = repo
        self._livro_id = livro_id
        self._livro_removido = None

    def executar(self):
        self._livro_removido = self._repo.buscar_por_id(self._livro_id)
        self._repo.deletar(self._livro_id)

    def desfazer(self):
        if self._livro_removido is not None:
            # reinsere preservando os dados (novo id sera gerado)
            self._repo.inserir(self._livro_removido)

    def descricao(self):
        return f"Deletar livro #{self._livro_id}"


class GerenciadorComandos:
    """Invoker: executa comandos e guarda historico para desfazer."""

    def __init__(self):
        self._historico = []

    def executar(self, comando):
        comando.executar()
        self._historico.append(comando)

    def pode_desfazer(self):
        return bool(self._historico)

    def desfazer_ultimo(self):
        if not self.pode_desfazer():
            return None
        comando = self._historico.pop()
        comando.desfazer()
        return comando.descricao()
