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

    def inserir(self, usuario):
        self._cursor.execute("""
            INSERT INTO usuario (nome, email, senha, telefone, cpf, tipo_acesso)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            usuario.nome, usuario.email, usuario.senha,
            usuario.telefone, usuario.cpf, usuario.tipo_acesso,
        ))
        self._db.commit()
        usuario.id = self._cursor.lastrowid
        return usuario.id

    def atualizar(self, usuario):
        self._cursor.execute("""
            UPDATE usuario SET
                nome = ?, email = ?, senha = ?, telefone = ?, cpf = ?, tipo_acesso = ?
            WHERE id = ?
        """, (
            usuario.nome, usuario.email, usuario.senha,
            usuario.telefone, usuario.cpf, usuario.tipo_acesso, usuario.id,
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

    def listar_todos(self):
        self._cursor.execute("SELECT * FROM usuario ORDER BY nome")
        return [self._para_entidade(row) for row in self._cursor.fetchall()]
