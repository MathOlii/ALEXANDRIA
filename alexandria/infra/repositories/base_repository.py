
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
