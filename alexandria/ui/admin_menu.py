"""Menu do administrador: CRUD completo de livros.

As acoes de escrita (inserir, atualizar, deletar) sao executadas via padrao
Command, atraves de um GerenciadorComandos que permite desfazer a ultima acao.
A construcao do Livro usa o padrao Builder.
"""
import tkinter as tk
from tkinter import messagebox, ttk

from alexandria.application.commands.livro_commands import (
    AtualizarLivroCommand,
    DeletarLivroCommand,
    GerenciadorComandos,
    InserirLivroCommand,
)
from alexandria.domain.builders.livro_builder import LivroBuilder
from alexandria.infra.repositories.livro_repository import LivroRepository

_CAMPOS = ["Titulo", "Autor", "Editora", "Genero", "Preco", "Estoque", "Ano", "Idioma"]
_COLUNAS = ("ID", "Titulo", "Autor", "Genero", "Preco", "Estoque", "Ano")


class AdminMenu:
    def __init__(self, main_window):
        self.main = main_window
        self.repo = LivroRepository()
        self.comandos = GerenciadorComandos()

        self.frame = tk.Frame(self.main.root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="MENU ADMIN", font=("Arial", 16)).pack(pady=10)

        busca = tk.Frame(self.frame)
        busca.pack()
        tk.Label(busca, text="Buscar:").pack(side="left")
        self.search = tk.Entry(busca)
        self.search.pack(side="left")
        tk.Button(busca, text="Pesquisar", command=self.buscar).pack(side="left")

        tk.Button(self.frame, text="Cadastrar Livro",
                  command=self.tela_cadastro).pack(pady=5)
        self.btn_delete = tk.Button(self.frame, text="Deletar Selecionado",
                                    command=self.deletar, state="disabled")
        self.btn_delete.pack(pady=5)
        self.btn_undo = tk.Button(self.frame, text="Desfazer ultima acao",
                                  command=self.desfazer, state="disabled")
        self.btn_undo.pack(pady=5)
        tk.Button(self.frame, text="Sair", command=self.sair).pack(pady=5)

        self.tree = ttk.Treeview(self.frame, columns=_COLUNAS, show="headings")
        for col in _COLUNAS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=70)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._atualizar_botoes)
        self.tree.bind("<Double-1>", self.editar)

        self.listar()

    # --- listagem ---
    def _inserir_linha(self, livro):
        self.tree.insert("", "end", values=(
            livro.id, livro.titulo, livro.autor, livro.genero,
            f"{livro.preco:.2f}", livro.estoque, livro.ano_publicacao,
        ))

    def listar(self):
        self.tree.delete(*self.tree.get_children())
        for livro in self.repo.listar_todos():
            self._inserir_linha(livro)
        self._atualizar_undo()

    def buscar(self):
        termo = self.search.get().lower()
        self.tree.delete(*self.tree.get_children())
        for livro in self.repo.listar_todos():
            alvo = f"{livro.titulo} {livro.autor} {livro.genero} {livro.editora}".lower()
            if termo in alvo:
                self._inserir_linha(livro)

    def _id_selecionado(self):
        selecao = self.tree.selection()
        if not selecao:
            return None
        return int(self.tree.item(selecao[0], "values")[0])

    def _atualizar_botoes(self, _event=None):
        estado = "normal" if self.tree.selection() else "disabled"
        self.btn_delete.config(state=estado)

    def _atualizar_undo(self):
        estado = "normal" if self.comandos.pode_desfazer() else "disabled"
        self.btn_undo.config(state=estado)

    # --- cadastro / edicao ---
    def tela_cadastro(self):
        self._tela_formulario("Cadastrar Livro", {}, self._salvar_novo)

    def editar(self, _event=None):
        livro_id = self._id_selecionado()
        if livro_id is None:
            return
        livro = self.repo.buscar_por_id(livro_id)
        valores = {
            "Titulo": livro.titulo, "Autor": livro.autor, "Editora": livro.editora,
            "Genero": livro.genero, "Preco": livro.preco, "Estoque": livro.estoque,
            "Ano": livro.ano_publicacao, "Idioma": livro.idioma,
        }
        self._tela_formulario(
            "Editar Livro", valores, lambda d: self._salvar_edicao(livro_id, d))

    def _tela_formulario(self, titulo, valores, ao_salvar):
        self.main.limpar()
        frame = tk.Frame(self.main.root)
        frame.pack(pady=10)
        tk.Label(frame, text=titulo, font=("Arial", 14)).pack(pady=5)

        entradas = {}
        for campo in _CAMPOS:
            tk.Label(frame, text=campo).pack()
            entry = tk.Entry(frame)
            if campo in valores and valores[campo] is not None:
                entry.insert(0, valores[campo])
            entry.pack()
            entradas[campo] = entry

        msg = tk.Label(frame, text="", fg="red")
        msg.pack()

        def salvar():
            try:
                ao_salvar({c: e.get() for c, e in entradas.items()})
                self.voltar()
            except Exception as erro:
                msg.config(text=str(erro))

        tk.Button(frame, text="Salvar", command=salvar).pack(pady=10)
        tk.Button(frame, text="Voltar", command=self.voltar).pack()

    def _montar_livro(self, dados, livro_id=None):
        builder = (LivroBuilder()
                   .com_titulo(dados["Titulo"]).com_autor(dados["Autor"])
                   .com_editora(dados["Editora"]).com_genero(dados["Genero"])
                   .com_preco(dados["Preco"]).com_estoque(dados["Estoque"])
                   .com_ano(dados["Ano"]).com_idioma(dados["Idioma"]))
        if livro_id is not None:
            builder.com_id(livro_id)
        return builder.construir()

    def _salvar_novo(self, dados):
        livro = self._montar_livro(dados)
        self.comandos.executar(InserirLivroCommand(self.repo, livro))

    def _salvar_edicao(self, livro_id, dados):
        livro = self._montar_livro(dados, livro_id)
        self.comandos.executar(AtualizarLivroCommand(self.repo, livro))

    # --- exclusao / undo ---
    def deletar(self):
        livro_id = self._id_selecionado()
        if livro_id is None:
            return
        if not messagebox.askyesno("Confirmar", "Deletar o livro selecionado?"):
            return
        self.comandos.executar(DeletarLivroCommand(self.repo, livro_id))
        self.listar()

    def desfazer(self):
        descricao = self.comandos.desfazer_ultimo()
        if descricao:
            messagebox.showinfo("Desfeito", f"Acao desfeita: {descricao}")
        self.listar()

    # --- navegacao ---
    def voltar(self):
        self.main.limpar()
        AdminMenu(self.main)

    def sair(self):
        self.main.usuario_logado = None
        self.main.mostrar_login()
