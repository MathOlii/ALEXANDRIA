"""Popula o catalogo com livros de exemplo.

Uso:
    python seed_livros.py
"""
from alexandria.domain.builders.livro_builder import LivroBuilder
from alexandria.infra.database_setup import criar_tabelas
from alexandria.infra.repositories.livro_repository import LivroRepository

# (titulo, autor, editora, genero, preco, ano)
_CATALOGO = [
    ("Duna", "Frank Herbert", "Aleph", "Ficcao Cientifica", 79.90, 1965),
    ("Messias de Duna", "Frank Herbert", "Aleph", "Ficcao Cientifica", 69.90, 1969),
    ("Fundacao", "Isaac Asimov", "Aleph", "Ficcao Cientifica", 59.90, 1951),
    ("A Sociedade do Anel", "J.R.R. Tolkien", "HarperCollins", "Fantasia", 79.90, 1954),
    ("As Duas Torres", "J.R.R. Tolkien", "HarperCollins", "Fantasia", 79.90, 1954),
    ("O Retorno do Rei", "J.R.R. Tolkien", "HarperCollins", "Fantasia", 79.90, 1955),
    ("1984", "George Orwell", "Companhia das Letras", "Distopia", 49.90, 1949),
    ("A Revolucao dos Bichos", "George Orwell", "Companhia das Letras", "Distopia", 39.90, 1945),
    ("Admiravel Mundo Novo", "Aldous Huxley", "Biblioteca Azul", "Distopia", 44.90, 1932),
    ("Fahrenheit 451", "Ray Bradbury", "Globo Livros", "Ficcao Cientifica", 49.90, 1953),
    ("O Principe", "Nicolau Maquiavel", "Martin Claret", "Filosofia", 29.90, 1532),
    ("A Arte da Guerra", "Sun Tzu", "Jardim dos Livros", "Estrategia", 24.90, -500),
    ("Meditacoes", "Marco Aurelio", "Edipro", "Filosofia", 34.90, 180),
    ("Pai Rico Pai Pobre", "Robert Kiyosaki", "Alta Books", "Financas", 59.90, 1997),
    ("Habitos Atomicos", "James Clear", "Alta Life", "Desenvolvimento Pessoal", 59.90, 2018),
    ("O Nome do Vento", "Patrick Rothfuss", "Arqueiro", "Fantasia", 59.90, 2007),
    ("A Guerra dos Tronos", "George R.R. Martin", "Suma", "Fantasia", 69.90, 1996),
    ("O Hobbit", "J.R.R. Tolkien", "HarperCollins", "Fantasia", 49.90, 1937),
    ("O Codigo Da Vinci", "Dan Brown", "Arqueiro", "Suspense", 49.90, 2003),
    ("Neuromancer", "William Gibson", "Aleph", "Ficcao Cientifica", 59.90, 1984),
    ("Eu, Robo", "Isaac Asimov", "Aleph", "Ficcao Cientifica", 49.90, 1950),
    ("Orgulho e Preconceito", "Jane Austen", "Martin Claret", "Romance", 34.90, 1813),
    ("A Culpa e das Estrelas", "John Green", "Intrinseca", "Romance", 39.90, 2012),
    ("It: A Coisa", "Stephen King", "Suma", "Terror", 79.90, 1986),
    ("O Iluminado", "Stephen King", "Suma", "Terror", 59.90, 1977),
    ("Dom Casmurro", "Machado de Assis", "Principis", "Classico", 24.90, 1899),
    ("Jogos Vorazes", "Suzanne Collins", "Rocco", "Aventura", 49.90, 2008),
    ("Dracula", "Bram Stoker", "Zahar", "Terror", 39.90, 1897),
    ("Frankenstein", "Mary Shelley", "Zahar", "Terror", 34.90, 1818),
    ("O Pequeno Principe", "Antoine de Saint-Exupery", "Agir", "Fabula", 29.90, 1943),
]

_ESTOQUE_PADRAO = 10


def seed_livros():
    criar_tabelas()
    repo = LivroRepository()
    for titulo, autor, editora, genero, preco, ano in _CATALOGO:
        livro = (LivroBuilder()
                 .com_titulo(titulo).com_autor(autor).com_editora(editora)
                 .com_genero(genero).com_preco(preco).com_estoque(_ESTOQUE_PADRAO)
                 .com_ano(ano).com_idioma("Portugues")
                 .construir())
        repo.inserir(livro)
    print(f"{len(_CATALOGO)} livros inseridos com sucesso!")


if __name__ == "__main__":
    seed_livros()
