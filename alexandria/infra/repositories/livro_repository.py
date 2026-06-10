
from alexandria.domain.entities.livro import Livro
from alexandria.infra.conexao import Conexao
from alexandria.infra.repositories.base_repository import BaseRepository


class LivroRepository(BaseRepository):
    def __init__(self):
        self._db = Conexao.instancia()
        self._cursor = self._db.cursor

    def _para_entidade(self, row):
        return Livro(*row[1:], id=row[0])

    def inserir(self, entidade):
        self._cursor.execute("""
            INSERT INTO livro
                (titulo, autor, editora, genero, preco, estoque, ano_publicacao, idioma)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entidade.titulo, entidade.autor, entidade.editora, entidade.genero,
            entidade.preco, entidade.estoque, entidade.ano_publicacao, entidade.idioma,
        ))
        self._db.commit()
        entidade.id = self._cursor.lastrowid

    def atualizar(self, entidade):
        self._cursor.execute("""
            UPDATE livro SET
                titulo = ?, autor = ?, editora = ?, genero = ?,
                preco = ?, estoque = ?, ano_publicacao = ?, idioma = ?
            WHERE id = ?
        """, (
            entidade.titulo, entidade.autor, entidade.editora, entidade.genero,
            entidade.preco, entidade.estoque, entidade.ano_publicacao, entidade.idioma,
            entidade.id,
        ))
        self._db.commit()

    def deletar(self, id):
        self._cursor.execute("DELETE FROM livro WHERE id = ?", (id,))
        self._db.commit()

    def buscar_por_id(self, id):  # type: ignore[override]
        self._cursor.execute("SELECT * FROM livro WHERE id = ?", (id,))
        row = self._cursor.fetchone()
        return self._para_entidade(row) if row else None

    def listar_todos(self) -> list['Livro']:  # type: ignore[override]
        self._cursor.execute("SELECT * FROM livro ORDER BY titulo")
        return [self._para_entidade(row) for row in self._cursor.fetchall()]
