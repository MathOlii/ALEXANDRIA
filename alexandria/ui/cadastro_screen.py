
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

        # Mascaras de formatacao em tempo real
        self.inputs["cpf"].bind("<KeyRelease>", self._mascara_cpf)
        self.inputs["telefone"].bind("<KeyRelease>", self._mascara_telefone)
        self.inputs["cep"].bind("<KeyRelease>", self._mascara_cep)

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

    # --- Mascaras de formatacao ---
    @staticmethod
    def _so_digitos(texto, maximo):
        return "".join(filter(str.isdigit, texto))[:maximo]

    def _aplicar(self, entry, texto):
        entry.delete(0, tk.END)
        entry.insert(0, texto)

    def _mascara_cpf(self, _event):
        d = self._so_digitos(self.inputs["cpf"].get(), 11)
        partes = [d[:3], d[3:6], d[6:9]]
        texto = ".".join(p for p in partes if p)
        if len(d) > 9:
            texto += "-" + d[9:]
        self._aplicar(self.inputs["cpf"], texto)

    def _mascara_telefone(self, _event):
        d = self._so_digitos(self.inputs["telefone"].get(), 11)
        texto = d[:2]
        if len(d) > 2:
            texto += " " + d[2:3]
        if len(d) > 3:
            texto += " " + d[3:7]
        if len(d) > 7:
            texto += "-" + d[7:11]
        self._aplicar(self.inputs["telefone"], texto)

    def _mascara_cep(self, _event):
        d = self._so_digitos(self.inputs["cep"].get(), 8)
        texto = d[:5]
        if len(d) > 5:
            texto += "-" + d[5:]
        self._aplicar(self.inputs["cep"], texto)

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
