"""Janela principal: gerencia a navegacao entre telas (tkinter)."""
import tkinter as tk

from alexandria.domain.entities.carrinho import Carrinho


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Alexandria")
        self.root.geometry("520x560")

        self.carrinho = Carrinho()
        self.usuario_logado = None

        self.mostrar_login()

    def limpar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        from alexandria.ui.login_screen import LoginScreen
        self.limpar()
        LoginScreen(self)

    def run(self):
        self.root.mainloop()
