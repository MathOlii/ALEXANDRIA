"""Repositorio de Endereco.

Lado "1" do relacionamento 1:1 com Usuario (usuario_id e UNIQUE).
"""
from alexandria.domain.entities.endereco import Endereco
from alexandria.infra.conexao import Conexao
from alexandria.infra.repositories.base_repository import BaseRepository


class EnderecoRepository(BaseRepository):
    def __init__(self):
        self._db = Conexao.instancia()
        self._cursor = self._db.cursor

    def _para_entidade(self, row):
        return Endereco(
            rua=row[1], numero=row[2], bairro=row[3], cep=row[4],
            cidade=row[5], uf=row[6], usuario_id=row[7], id=row[0],
        )

    def inserir(self, endereco):
        self._cursor.execute("""
            INSERT INTO endereco (rua, numero, bairro, cep, cidade, uf, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            endereco.rua, endereco.numero, endereco.bairro, endereco.cep,
            endereco.cidade, endereco.uf, endereco.usuario_id,
        ))
        self._db.commit()
        endereco.id = self._cursor.lastrowid
        return endereco.id

    def atualizar(self, endereco):
        self._cursor.execute("""
            UPDATE endereco SET
                rua = ?, numero = ?, bairro = ?, cep = ?, cidade = ?, uf = ?
            WHERE id = ?
        """, (
            endereco.rua, endereco.numero, endereco.bairro, endereco.cep,
            endereco.cidade, endereco.uf, endereco.id,
        ))
        self._db.commit()

    def deletar(self, id):
        self._cursor.execute("DELETE FROM endereco WHERE id = ?", (id,))
        self._db.commit()

    def buscar_por_id(self, id):
        self._cursor.execute("SELECT * FROM endereco WHERE id = ?", (id,))
        row = self._cursor.fetchone()
        return self._para_entidade(row) if row else None

    def buscar_por_usuario(self, usuario_id):
        self._cursor.execute(
            "SELECT * FROM endereco WHERE usuario_id = ?", (usuario_id,))
        row = self._cursor.fetchone()
        return self._para_entidade(row) if row else None

    def listar_todos(self):
        self._cursor.execute("SELECT * FROM endereco")
        return [self._para_entidade(row) for row in self._cursor.fetchall()]
