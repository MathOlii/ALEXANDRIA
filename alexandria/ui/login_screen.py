
import tkinter as tk

from alexandria.application.services.auth_service import (
    AuthService,
    CredenciaisInvalidas,
)


class LoginScreen:
    def __init__(self, main_window):
        self.main = main_window
        self.auth = AuthService()

        frame = tk.Frame(self.main.root)
        frame.pack(expand=True)

        tk.Label(frame, text="ALEXANDRIA", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(frame, text="Login", font=("Arial", 14)).pack(pady=5)

        tk.Label(frame, text="Email").pack()
        self.email = tk.Entry(frame, width=30)
        self.email.pack(pady=5)

        tk.Label(frame, text="Senha").pack()
        self.senha = tk.Entry(frame, show="*", width=30)
        self.senha.pack(pady=5)

        self.msg = tk.Label(frame, text="", fg="red")
        self.msg.pack()

        tk.Button(frame, text="Entrar", width=20, command=self.login).pack(pady=10)
        tk.Button(frame, text="Cadastrar", width=20,
                  command=self.ir_para_cadastro).pack()

    def login(self):
        try:
            usuario = self.auth.autenticar(self.email.get(), self.senha.get())
        except CredenciaisInvalidas as erro:
            self.msg.config(text=str(erro))
            return

        self.main.usuario_logado = usuario
        self.main.limpar()

        if usuario.eh_admin():
            from alexandria.ui.admin_menu import AdminMenu
            AdminMenu(self.main)
        else:
            from alexandria.ui.cliente_menu import ClienteMenu
            ClienteMenu(self.main)

    def ir_para_cadastro(self):
        from alexandria.ui.cadastro_screen import CadastroScreen
        self.main.limpar()
        CadastroScreen(self.main)
