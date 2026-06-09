"""Configuracoes e constantes do sistema.

Centralizar valores aqui evita "numeros magicos" espalhados pelo codigo
(Calistenia de Objetos) e deixa as regras de negocio explicitas.
"""
from pathlib import Path

# Caminho do banco SQLite, sempre relativo a raiz do projeto.
RAIZ_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = str(RAIZ_PROJETO / "alexandria.db")

# Regras de validacao.
TAMANHO_MINIMO_SENHA = 6
TAMANHO_CPF = 11
TAMANHO_TELEFONE = 11
TAMANHO_CEP = 8

# Regras de precificacao do pedido (usadas pelos Decorators).
ALIQUOTA_IMPOSTO = 0.05            # 5% de imposto sobre o subtotal
VALOR_FRETE_PADRAO = 15.00         # frete fixo
VALOR_FRETE_GRATIS_ACIMA_DE = 200.00   # frete gratis a partir deste total
QTD_MINIMA_DESCONTO_PROGRESSIVO = 5     # itens para ganhar desconto progressivo
PERCENTUAL_DESCONTO_PROGRESSIVO = 0.10  # 10% de desconto

UFS_VALIDAS = (
    "AC", "AP", "AM", "PA", "RO", "RR", "TO",
    "AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE",
    "DF", "GO", "MT", "MS",
    "ES", "MG", "RJ", "SP",
    "PR", "RS", "SC",
)
