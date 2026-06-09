"""Criacao das tabelas do banco em um unico lugar.

No projeto original a criacao de tabelas estava duplicada entre
``tabelas_livros`` e ``tabelas_pedidos``, e havia a tabela ``usuario_completo``
que nunca era usada. Aqui tudo fica centralizado e sem duplicacao (DRY).
"""
from alexandria.infra.conexao import Conexao

_TABELAS = (
    """
    CREATE TABLE IF NOT EXISTS livro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        editora TEXT,
        genero TEXT,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL,
        ano_publicacao INTEGER,
        idioma TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS usuario (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        telefone TEXT,
        cpf TEXT,
        tipo_acesso TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS endereco (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rua TEXT,
        numero TEXT,
        bairro TEXT,
        cep TEXT,
        cidade TEXT,
        uf TEXT,
        usuario_id INTEGER UNIQUE,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        total REAL NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuario(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS item_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        livro_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE,
        FOREIGN KEY (livro_id) REFERENCES livro(id)
    )
    """,
)


def criar_tabelas():
    db = Conexao.instancia()
    for comando in _TABELAS:
        db.cursor.execute(comando)
    db.commit()
