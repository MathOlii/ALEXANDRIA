"""Interface base dos repositorios (CRUD).

Define o contrato comum esperado pelos servicos. Os servicos dependem desta
abstracao, nao das implementacoes concretas (DIP). Manter a interface enxuta
atende ao ISP.
"""
from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def inserir(self, entidade):
        ...

    @abstractmethod
    def atualizar(self, entidade):
        ...

    @abstractmethod
    def deletar(self, id):
        ...

    @abstractmethod
    def buscar_por_id(self, id):
        ...

    @abstractmethod
    def listar_todos(self):
        ...
