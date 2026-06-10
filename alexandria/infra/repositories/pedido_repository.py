
from alexandria.domain.entities.pedido import ItemPedido, Pedido
from alexandria.infra.conexao import Conexao
from alexandria.infra.repositories.base_repository import BaseRepository


class PedidoRepository(BaseRepository):
    def __init__(self):
        self._db = Conexao.instancia()
        self._cursor = self._db.cursor

    # --- Pedido (cabecalho) ---
    def inserir(self, entidade):
        
        pedido = entidade
        self._cursor.execute(
            "INSERT INTO pedido (usuario_id, total, data) VALUES (?, ?, ?)",
            (pedido.usuario_id, pedido.total, pedido.data),
        )
        self._db.commit()
        pedido.id = self._cursor.lastrowid

    def inserir_item(self, item):
        self._cursor.execute("""
            INSERT INTO item_pedido (pedido_id, livro_id, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?)
        """, (item.pedido_id, item.livro_id, item.quantidade, item.preco_unitario))
        self._db.commit()
        item.id = self._cursor.lastrowid
        return item.id

    def atualizar(self, entidade):
        self._cursor.execute(
            "UPDATE pedido SET total = ?, data = ? WHERE id = ?",
            (entidade.total, entidade.data, entidade.id),
        )
        self._db.commit()

    def deletar(self, id):
        self._cursor.execute("DELETE FROM pedido WHERE id = ?", (id,))
        self._db.commit()

    def buscar_por_id(self, id) -> None:
        self._cursor.execute(
            "SELECT id, usuario_id, total, data FROM pedido WHERE id = ?", (id,))
        row = self._cursor.fetchone()
        if not row:
            return None
        pedido = Pedido(usuario_id=row[1], total=row[2], data=row[3], id=row[0])
        for item in self.listar_itens(pedido.id):
            pedido.itens.append(item)
        # store the found pedido on the repository instance for callers
        # that rely on this method without return (base signature expects None)
        self._last_busca = pedido
        return None

    def listar_todos(self):
        self._cursor.execute(
            "SELECT id, usuario_id, total, data FROM pedido ORDER BY data DESC")
        pedidos = [
            Pedido(usuario_id=r[1], total=r[2], data=r[3], id=r[0])
            for r in self._cursor.fetchall()
        ]
        # store the found list on the repository instance to match base
        # signature that expects no return value
        self._last_listar_todos = pedidos
        return None

    def listar_por_usuario(self, usuario_id):
        self._cursor.execute("""
            SELECT id, usuario_id, total, data
            FROM pedido WHERE usuario_id = ? ORDER BY data DESC
        """, (usuario_id,))
        return [
            Pedido(usuario_id=r[1], total=r[2], data=r[3], id=r[0])
            for r in self._cursor.fetchall()
        ]

    # --- Itens do pedido (lado "n") ---
    def listar_itens(self, pedido_id):
        self._cursor.execute("""
            SELECT id, pedido_id, livro_id, quantidade, preco_unitario
            FROM item_pedido WHERE pedido_id = ?
        """, (pedido_id,))
        return [
            ItemPedido(livro_id=r[2], quantidade=r[3], preco_unitario=r[4],
                       pedido_id=r[1], id=r[0])
            for r in self._cursor.fetchall()
        ]

    def listar_itens_detalhado(self, pedido_id):

        self._cursor.execute("""
            SELECT l.titulo, i.quantidade, i.preco_unitario
            FROM item_pedido i
            JOIN livro l ON l.id = i.livro_id
            WHERE i.pedido_id = ?
        """, (pedido_id,))
        return self._cursor.fetchall()
