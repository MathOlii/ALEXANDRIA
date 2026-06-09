"""Carrinho de compras.

Calistenia de Objetos: o Carrinho e uma "colecao de primeira classe" -
encapsula a lista de itens e expoe operacoes de negocio em vez de deixar
a lista crua exposta.
"""


class ItemCarrinho:
    def __init__(self, livro, quantidade=1):
        self.livro = livro
        self.quantidade = quantidade

    def subtotal(self):
        return self.livro.preco * self.quantidade


class Carrinho:
    def __init__(self):
        self._itens = []

    @property
    def itens(self):
        return tuple(self._itens)

    def esta_vazio(self):
        return not self._itens

    def quantidade_total(self):
        return sum(item.quantidade for item in self._itens)

    def adicionar(self, livro):
        for item in self._itens:
            if item.livro.id == livro.id:
                item.quantidade += 1
                return
        self._itens.append(ItemCarrinho(livro))

    def remover(self, livro_id):
        self._itens = [i for i in self._itens if i.livro.id != livro_id]

    def subtotal(self):
        return sum(item.subtotal() for item in self._itens)

    def limpar(self):
        self._itens = []
