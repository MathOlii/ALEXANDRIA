"""Servico de autenticacao e cadastro.

No projeto original o AuthService usava input()/print() diretamente,
misturando interface com regra de negocio (violacao de SRP). Aqui o servico
recebe apenas dados e devolve resultados/excecoes; quem coleta os dados e a
camada de UI. As dependencias (repositorios) sao injetadas (DIP).
"""
import hashlib

from alexandria.application.validacao.validadores import ValidadorCadastro
from alexandria.domain.entities.endereco import Endereco
from alexandria.domain.value_objects import Cep, Cpf, Email, Telefone, Uf
from alexandria.factories.usuario_factory import UsuarioFactory
from alexandria.infra.repositories.endereco_repository import EnderecoRepository
from alexandria.infra.repositories.usuario_repository import UsuarioRepository


class CredenciaisInvalidas(Exception):
    pass


class DadosInvalidos(Exception):
    def __init__(self, erros):
        self.erros = erros
        super().__init__("; ".join(erros))


class AuthService:
    def __init__(self, usuario_repo=None, endereco_repo=None, validador=None):
        self._usuario_repo = usuario_repo or UsuarioRepository()
        self._endereco_repo = endereco_repo or EnderecoRepository()
        self._validador = validador or ValidadorCadastro()

    @staticmethod
    def _criptografar(senha):
        return hashlib.sha256(senha.encode()).hexdigest()

    def cadastrar(self, dados):
        """Cadastra usuario + endereco (relacionamento 1:1).

        `dados` e um dict com os campos do formulario. Levanta DadosInvalidos
        se a validacao falhar.
        """
        erros = self._validador.validar(dados)
        if erros:
            raise DadosInvalidos(erros)

        if self._usuario_repo.buscar_por_email(Email(dados["email"]).valor):
            raise DadosInvalidos(["Ja existe um usuario com este email."])

        usuario = UsuarioFactory.criar(
            tipo=dados["tipo"],
            nome=dados["nome"].strip(),
            email=Email(dados["email"]).valor,
            senha=self._criptografar(dados["senha"]),
            telefone=Telefone(dados["telefone"]).valor,
            cpf=Cpf(dados["cpf"]).valor,
        )
        usuario_id = self._usuario_repo.inserir(usuario)

        endereco = Endereco(
            rua=dados["rua"], numero=dados["numero"], bairro=dados["bairro"],
            cep=Cep(dados["cep"]).valor, cidade=dados["cidade"],
            uf=Uf(dados["uf"]).valor, usuario_id=usuario_id,
        )
        self._endereco_repo.inserir(endereco)
        return usuario

    def autenticar(self, email, senha):
        """Retorna o Usuario autenticado ou levanta CredenciaisInvalidas."""
        try:
            email_normalizado = Email(email).valor
        except Exception:
            raise CredenciaisInvalidas("Email ou senha invalidos.")

        usuario = self._usuario_repo.buscar_por_email(email_normalizado)
        if not usuario or usuario.senha != self._criptografar(senha):
            raise CredenciaisInvalidas("Email ou senha invalidos.")
        return usuario
