"""Conexao unica com o banco de dados (padrao Singleton)."""
import sqlite3

from alexandria.config import CAMINHO_BANCO


class Conexao:

    _instancia = None

    def __init__(self):
        self.conn = sqlite3.connect(CAMINHO_BANCO)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()

    @classmethod
    def instancia(cls):
        if cls._instancia is None:
            cls._instancia = Conexao()
        return cls._instancia

    def commit(self):
        self.conn.commit()

    def fechar(self):
        self.conn.close()
        Conexao._instancia = None
