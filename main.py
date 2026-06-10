
from alexandria.infra.database_setup import criar_tabelas
from alexandria.ui.main_window import MainWindow


def main():
    criar_tabelas()
    MainWindow().run()


if __name__ == "__main__":
    main()
