from alexandria.domain.entities.livro import Livro

_ANO_MINIMO = -3000
_ANO_MAXIMO = 2100


class LivroBuilder:
    def __init__(self):
        self._dados = {
            "titulo": None,
            "autor": None,
            "editora": "",
            "genero": "",
            "preco": None,
            "estoque": 0,
            "ano_publicacao": None,
            "idioma": "Portugues",
        }
        self._id = None

    def com_titulo(self, titulo):
        self._dados["titulo"] = (titulo or "").strip()
        return self

    def com_autor(self, autor):
        self._dados["autor"] = (autor or "").strip()
        return self

    def com_editora(self, editora):
        self._dados["editora"] = (editora or "").strip()
        return self

    def com_genero(self, genero):
        self._dados["genero"] = (genero or "").strip()
        return self

    def com_preco(self, preco):
        try:
            self._dados["preco"] = float(str(preco).replace(",", ".").strip())
        except (TypeError, ValueError):
            raise ValueError("Preco deve ser um numero decimal (ex: 49.90).")
        return self

    def com_estoque(self, estoque):
        try:
            self._dados["estoque"] = int(str(estoque).strip())
        except (TypeError, ValueError):
            raise ValueError("Estoque deve ser um numero inteiro (ex: 10).")
        return self

    def com_ano(self, ano):
        try:
            self._dados["ano_publicacao"] = int(str(ano).strip())
        except (TypeError, ValueError):
            raise ValueError("Ano deve ser um numero inteiro (ex: 1965).")
        return self

    def com_idioma(self, idioma):
        self._dados["idioma"] = (idioma or "").strip()
        return self

    def com_id(self, id):
        self._id = id
        return self

    def _validar(self):
        if not self._dados["titulo"]:
            raise ValueError("Titulo e obrigatorio.")
        if not self._dados["autor"]:
            raise ValueError("Autor e obrigatorio.")
        if self._dados["preco"] is None or self._dados["preco"] <= 0:
            raise ValueError("Preco deve ser maior que zero.")
        if self._dados["estoque"] < 0:
            raise ValueError("Estoque nao pode ser negativo.")
        ano = self._dados["ano_publicacao"]
        if ano is not None and not (_ANO_MINIMO <= ano <= _ANO_MAXIMO):
            raise ValueError("Ano de publicacao invalido.")

    def construir(self):
        self._validar()
        return Livro(id=self._id, **self._dados)
