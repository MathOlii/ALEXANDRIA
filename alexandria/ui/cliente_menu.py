"""Menu do cliente: catalogo, carrinho, cupom e pedidos.

A tela do carrinho mostra o detalhamento do preco calculado pela cadeia de
Decorators (subtotal -> descontos -> imposto -> frete).
"""
import tkinter as tk
from tkinter import messagebox, ttk

from alexandria.application.services.pedido_service import (
    CarrinhoVazio,
    CupomInvalido,
    PedidoService,
)
from alexandria.infra.repositories.livro_repository import LivroRepository

_COLUNAS = ("ID", "Titulo", "Autor", "Genero", "Preco", "Estoque")


class ClienteMenu:
    def __init__(self, main_window):
        self.main = main_window
        self.repo = LivroRepository()
        self.service = PedidoService()
        self.carrinho = self.main.carrinho

        self.frame = tk.Frame(self.main.root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="MENU CLIENTE", font=("Arial", 16)).pack(pady=10)

        busca = tk.Frame(self.frame)
        busca.pack(pady=5)
        tk.Label(busca, text="Buscar:").pack(side="left")
        self.search = tk.Entry(busca)
        self.search.pack(side="left", padx=5)
        tk.Button(busca, text="Pesquisar", command=self.pesquisar).pack(side="left")

        self.tree = ttk.Treeview(self.frame, columns=_COLUNAS, show="headings")
        for col in _COLUNAS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80)
        self.tree.pack(fill="both", expand=True)

        tk.Button(self.frame, text="Adicionar ao Carrinho",
                  command=self.add_carrinho).pack(pady=2)
        tk.Button(self.frame, text="Ver Carrinho",
                  command=self.ver_carrinho).pack(pady=2)
        tk.Button(self.frame, text="Meus Pedidos",
                  command=self.meus_pedidos).pack(pady=2)
        tk.Button(self.frame, text="Sair", command=self.sair).pack(pady=2)

        self.listar()

    def _inserir_linha(self, livro):
        self.tree.insert("", "end", values=(
            livro.id, livro.titulo, livro.autor, livro.genero,
            f"R$ {livro.preco:.2f}", livro.estoque,
        ))

    def listar(self, filtro=None):
        self.tree.delete(*self.tree.get_children())
        for livro in self.repo.listar_todos():
            if filtro is None or filtro in f"{livro.titulo} {livro.autor}".lower():
                self._inserir_linha(livro)

    def pesquisar(self):
        self.listar(self.search.get().lower())

    def _livro_selecionado(self):
        selecao = self.tree.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um livro.")
            return None
        livro_id = int(self.tree.item(selecao[0], "values")[0])
        return self.repo.buscar_por_id(livro_id)

    def add_carrinho(self):
        livro = self._livro_selecionado()
        if livro:
            self.carrinho.adicionar(livro)
            messagebox.showinfo("Sucesso", "Livro adicionado ao carrinho!")

    # --- carrinho ---
    def ver_carrinho(self):
        self.main.limpar()
        frame = tk.Frame(self.main.root)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="CARRINHO", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(frame, columns=("Titulo", "Qtd", "Subtotal"),
                            show="headings")
        for col in ("Titulo", "Qtd", "Subtotal"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)
        for item in self.carrinho.itens:
            tree.insert("", "end", values=(
                item.livro.titulo, item.quantidade, f"R$ {item.subtotal():.2f}"))

        tk.Label(frame, text="Cupom (opcional):").pack()
        cupom_entry = tk.Entry(frame)
        cupom_entry.pack()

        resumo = tk.Label(frame, text="", justify="left", font=("Consolas", 10))
        resumo.pack(pady=5)

        def calcular():
            try:
                calculo = self.service.montar_calculo(
                    self.carrinho, cupom_entry.get() or None)
                resumo.config(
                    text=f"{calculo.descricao()}\nTOTAL: R$ {calculo.calcular():.2f}",
                    fg="black")
            except CupomInvalido as erro:
                resumo.config(text=str(erro), fg="red")

        def finalizar():
            try:
                pedido_id = self.service.finalizar_pedido(
                    self.main.usuario_logado.id, self.carrinho,
                    cupom_entry.get() or None)
                messagebox.showinfo("Sucesso", f"Pedido #{pedido_id} realizado!")
                self.voltar()
            except (CarrinhoVazio, CupomInvalido, ValueError) as erro:
                messagebox.showerror("Erro", str(erro))

        tk.Button(frame, text="Calcular Total", command=calcular).pack(pady=2)
        tk.Button(frame, text="Finalizar Pedido", command=finalizar).pack(pady=2)
        tk.Button(frame, text="Voltar", command=self.voltar).pack(pady=2)

        calcular()

    # --- pedidos ---
    def meus_pedidos(self):
        self.main.limpar()
        frame = tk.Frame(self.main.root)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="MEUS PEDIDOS", font=("Arial", 16)).pack(pady=10)

        tree = ttk.Treeview(frame, columns=("ID", "Total", "Data"), show="headings")
        for col in ("ID", "Total", "Data"):
            tree.heading(col, text=col)
        tree.pack(fill="both", expand=True)

        pedidos = self.service.listar_pedidos_do_usuario(self.main.usuario_logado.id)
        for pedido in pedidos:
            tree.insert("", "end", values=(
                pedido.id, f"R$ {pedido.total:.2f}", pedido.data))

        def ver_itens(_event):
            selecao = tree.selection()
            if not selecao:
                return
            pedido_id = int(tree.item(selecao[0], "values")[0])
            itens = self.service.itens_do_pedido(pedido_id)
            texto = "\n".join(
                f"{titulo} | Qtd: {qtd} | R$ {preco:.2f}"
                for titulo, qtd, preco in itens) or "Nenhum item."
            messagebox.showinfo(f"Pedido {pedido_id}", texto)

        tree.bind("<Double-1>", ver_itens)
        tk.Button(frame, text="Voltar", command=self.voltar).pack(pady=10)

    # --- navegacao ---
    def voltar(self):
        self.main.limpar()
        ClienteMenu(self.main)

    def sair(self):
        self.main.usuario_logado = None
        self.carrinho.limpar()
        self.main.mostrar_login()
