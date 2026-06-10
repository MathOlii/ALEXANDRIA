"""Repositorio de Usuario: CRUD completo.

Reconstroi a subclasse correta (Cliente/Administrador) via UsuarioFactory ao
ler do banco, eliminando os "indices magicos" (user[3], user[6]) que existiam
no projeto original.
"""
from alexandria.domain.entities.usuario import Usuario
from alexandria.factories.usuario_factory import UsuarioFactory
from alexandria.infra.conexao import Conexao
from alexandria.infra.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository):
    def __init__(self):
        self._db = Conexao.instancia()
        self._cursor = self._db.cursor

    def _para_entidade(self, row):
        # row: (id, nome, email, senha, telefone, cpf, tipo_acesso)
        return UsuarioFactory.criar(
            tipo=row[6],
            nome=row[1],
            email=row[2],
            senha=row[3],
            telefone=row[4],
            cpf=row[5],
            id=row[0],
        )

    def inserir(self, entidade):
        self._cursor.execute("""
            INSERT INTO usuario (nome, email, senha, telefone, cpf, tipo_acesso)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            entidade.nome, entidade.email, entidade.senha,
            entidade.telefone, entidade.cpf, entidade.tipo_acesso,
        ))
        self._db.commit()
        entidade.id = self._cursor.lastrowid

    def atualizar(self, entidade):
        self._cursor.execute("""
            UPDATE usuario SET
                nome = ?, email = ?, senha = ?, telefone = ?, cpf = ?, tipo_acesso = ?
            WHERE id = ?
        """, (
            entidade.nome, entidade.email, entidade.senha,
            entidade.telefone, entidade.cpf, entidade.tipo_acesso, entidade.id,
        ))
        self._db.commit()

    def deletar(self, id):
        self._cursor.execute("DELETE FROM usuario WHERE id = ?", (id,))
        self._db.commit()

    def buscar_por_id(self, id):
        self._cursor.execute("SELECT * FROM usuario WHERE id = ?", (id,))
        row = self._cursor.fetchone()
        return self._para_entidade(row) if row else None

    def buscar_por_email(self, email):
        self._cursor.execute("SELECT * FROM usuario WHERE email = ?", (email,))
        row = self._cursor.fetchone()
        return self._para_entidade(row) if row else None

    def listar_todos(self):  # type: ignore[override]
        self._cursor.execute("SELECT * FROM usuario ORDER BY nome")
        return [self._para_entidade(row) for row in self._cursor.fetchall()]
