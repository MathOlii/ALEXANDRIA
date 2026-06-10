from abc import ABC, abstractmethod

from alexandria.config import (
    ALIQUOTA_IMPOSTO,
    PERCENTUAL_DESCONTO_PROGRESSIVO,
    QTD_MINIMA_DESCONTO_PROGRESSIVO,
    VALOR_FRETE_GRATIS_ACIMA_DE,
    VALOR_FRETE_PADRAO,
)


class CalculoPreco(ABC):
    @abstractmethod
    def calcular(self) -> float:
        pass

    @abstractmethod
    def descricao(self) -> str:
        pass


class PrecoBaseCarrinho(CalculoPreco):

    def __init__(self, carrinho):
        self._carrinho = carrinho

    def calcular(self):
        return self._carrinho.subtotal()

    def descricao(self):
        return f"Subtotal: R$ {self.calcular():.2f}"


class DecoradorPreco(CalculoPreco):

    def __init__(self, componente):
        self._componente = componente

    def calcular(self):
        return self._componente.calcular()

    def descricao(self):
        return self._componente.descricao()


class DescontoProgressivo(DecoradorPreco):

    def __init__(self, componente, quantidade_itens):
        super().__init__(componente)
        self._quantidade_itens = quantidade_itens

    def _aplica_desconto(self):
        return self._quantidade_itens >= QTD_MINIMA_DESCONTO_PROGRESSIVO

    def calcular(self):
        valor = self._componente.calcular()
        if self._aplica_desconto():
            return valor * (1 - PERCENTUAL_DESCONTO_PROGRESSIVO)
        return valor

    def descricao(self):
        if not self._aplica_desconto():
            return self._componente.descricao()
        percentual = int(PERCENTUAL_DESCONTO_PROGRESSIVO * 100)
        return (f"{self._componente.descricao()}\n"
                f"Desconto progressivo ({percentual}%): -R$ "
                f"{self._componente.calcular() * PERCENTUAL_DESCONTO_PROGRESSIVO:.2f}")


class CupomDesconto(DecoradorPreco):

    def __init__(self, componente, codigo, percentual):
        super().__init__(componente)
        self._codigo = codigo
        self._percentual = percentual

    def calcular(self):
        return self._componente.calcular() * (1 - self._percentual)

    def descricao(self):
        valor_desconto = self._componente.calcular() * self._percentual
        percentual = int(self._percentual * 100)
        return (f"{self._componente.descricao()}\n"
                f"Cupom {self._codigo} ({percentual}%): -R$ {valor_desconto:.2f}")


class Imposto(DecoradorPreco):

    def calcular(self):
        valor = self._componente.calcular()
        return valor * (1 + ALIQUOTA_IMPOSTO)

    def descricao(self):
        valor_imposto = self._componente.calcular() * ALIQUOTA_IMPOSTO
        percentual = int(ALIQUOTA_IMPOSTO * 100)
        return (f"{self._componente.descricao()}\n"
                f"Imposto ({percentual}%): +R$ {valor_imposto:.2f}")


class Frete(DecoradorPreco):

    def _valor_frete(self):
        if self._componente.calcular() >= VALOR_FRETE_GRATIS_ACIMA_DE:
            return 0.0
        return VALOR_FRETE_PADRAO

    def calcular(self):
        return self._componente.calcular() + self._valor_frete()

    def descricao(self):
        frete = self._valor_frete()
        if frete == 0.0:
            return f"{self._componente.descricao()}\nFrete: GRATIS"
        return f"{self._componente.descricao()}\nFrete: +R$ {frete:.2f}"
