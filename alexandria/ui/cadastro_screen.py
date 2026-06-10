
import tkinter as tk

from alexandria.application.services.auth_service import (
    AuthService,
    DadosInvalidos,
)


class CadastroScreen:
    _CAMPOS_PESSOAIS = [
        ("nome", "Nome", False),
        ("email", "Email", False),
        ("senha", "Senha", True),
        ("telefone", "Telefone", False),
        ("cpf", "CPF", False),
    ]
    _CAMPOS_ENDERECO = [
        ("rua", "Rua"),
        ("numero", "Numero"),
        ("bairro", "Bairro"),
        ("cep", "CEP"),
        ("cidade", "Cidade"),
        ("uf", "UF"),
    ]

    def __init__(self, main_window):
        self.main = main_window
        self.auth = AuthService()
        self.inputs = {}

        frame = tk.Frame(self.main.root)
        frame.pack(expand=True, pady=10)

        tk.Label(frame, text="Cadastro", font=("Arial", 16)).pack(pady=5)

        tk.Label(frame, text="--- Dados pessoais ---").pack()
        for chave, rotulo, secreto in self._CAMPOS_PESSOAIS:
            self.inputs[chave] = self._criar_input(frame, rotulo, secreto)

        tk.Label(frame, text="--- Endereco ---").pack(pady=5)
        for chave, rotulo in self._CAMPOS_ENDERECO:
            self.inputs[chave] = self._criar_input(frame, rotulo, False)

        self.tipo = tk.StringVar(value="cliente")
        tk.Label(frame, text="Tipo de Usuario").pack()
        tk.Radiobutton(frame, text="Cliente", variable=self.tipo,
                       value="cliente").pack()
        tk.Radiobutton(frame, text="Admin", variable=self.tipo,
                       value="admin").pack()

        self.msg = tk.Label(frame, text="", fg="red", wraplength=400, justify="left")
        self.msg.pack(pady=5)

        tk.Button(frame, text="Cadastrar", command=self.cadastrar).pack(pady=5)
        tk.Button(frame, text="Voltar", command=self.voltar).pack()

    def _criar_input(self, frame, rotulo, secreto):
        container = tk.Frame(frame)
        container.pack(pady=2)
        tk.Label(container, text=rotulo, width=12, anchor="w").pack(side="left")
        entry = tk.Entry(container, width=28, show="*" if secreto else "")
        entry.pack(side="left")
        return entry

    def cadastrar(self):
        dados = {chave: entry.get() for chave, entry in self.inputs.items()}
        dados["tipo"] = self.tipo.get()
        try:
            self.auth.cadastrar(dados)
            self.msg.config(text="Cadastro realizado com sucesso!", fg="green")
        except DadosInvalidos as erro:
            self.msg.config(text="\n".join(erro.erros), fg="red")

    def voltar(self):
        self.main.mostrar_login()
