"""Entidades de pedido (lado "1") e item de pedido (lado "n")."""


class Pedido:
    def __init__(self, usuario_id, total, data, id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.total = total
        self.data = data
        self.itens = []

    def adicionar_item(self, item):
        item.pedido_id = self.id
        self.itens.append(item)


class ItemPedido:
    def __init__(self, livro_id, quantidade, preco_unitario,
                 pedido_id=None, id=None):
        self.id = id
        self.pedido_id = pedido_id
        self.livro_id = livro_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

    def subtotal(self):
        return self.preco_unitario * self.quantidade
