"""Ponto de entrada do sistema Alexandria.

Cria as tabelas (idempotente) e inicia a interface grafica.
"""
from alexandria.infra.database_setup import criar_tabelas
from alexandria.ui.main_window import MainWindow


def main():
    criar_tabelas()
    MainWindow().run()


if __name__ == "__main__":
    main()
