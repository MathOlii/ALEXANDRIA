
from typing import List, Optional

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

    def inserir(self, entidade):
        self._cursor.execute("""
            INSERT INTO endereco (rua, numero, bairro, cep, cidade, uf, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            entidade.rua, entidade.numero, entidade.bairro, entidade.cep,
            entidade.cidade, entidade.uf, entidade.usuario_id,
        ))
        self._db.commit()
        entidade.id = self._cursor.lastrowid
        return None

    def atualizar(self, entidade):
        self._cursor.execute("""
            UPDATE endereco SET
                rua = ?, numero = ?, bairro = ?, cep = ?, cidade = ?, uf = ?
            WHERE id = ?
        """, (
            entidade.rua, entidade.numero, entidade.bairro, entidade.cep,
            entidade.cidade, entidade.uf, entidade.id,
        ))
        self._db.commit()

    def deletar(self, id):
        self._cursor.execute("DELETE FROM endereco WHERE id = ?", (id,))
        self._db.commit()

    def buscar_por_id(self, id):  # type: ignore[override]
        self._cursor.execute("SELECT * FROM endereco WHERE id = ?", (id,))
        row = self._cursor.fetchone()
        return self._para_entidade(row) if row else None

    def buscar_por_usuario(self, usuario_id) -> Optional[Endereco]:
        self._cursor.execute(
            "SELECT * FROM endereco WHERE usuario_id = ?", (usuario_id,))
        row = self._cursor.fetchone()
        return self._para_entidade(row) if row else None

    def listar_todos(self) -> List[Endereco]:  # type: ignore[override]
        self._cursor.execute("SELECT * FROM endereco")
        return [self._para_entidade(row) for row in self._cursor.fetchall()]
