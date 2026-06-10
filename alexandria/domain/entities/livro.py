class Livro:
    def __init__(self, titulo, autor, editora, genero, preco, estoque,
                 ano_publicacao, idioma, id=None):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.genero = genero
        self.preco = preco
        self.estoque = estoque
        self.ano_publicacao = ano_publicacao
        self.idioma = idioma

    def tem_estoque_para(self, quantidade):
        return self.estoque >= quantidade

    def baixar_estoque(self, quantidade):
        if not self.tem_estoque_para(quantidade):
            raise ValueError(f"Estoque insuficiente para '{self.titulo}'.")
        self.estoque -= quantidade

    def __str__(self):
        return (f"[{self.id}] {self.titulo} - {self.autor} "
                f"| R$ {self.preco:.2f} | Estoque: {self.estoque}")
