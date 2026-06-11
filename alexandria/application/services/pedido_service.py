
from datetime import datetime

from alexandria.domain.entities.pedido import ItemPedido, Pedido
from alexandria.domain.pricing.calculo_preco import (
    CupomDesconto,
    DescontoProgressivo,
    Frete,
    Imposto,
    PrecoBaseCarrinho,
)
from alexandria.domain.pricing.cupons import percentual_do_cupom
from alexandria.infra.repositories.livro_repository import LivroRepository
from alexandria.infra.repositories.pedido_repository import PedidoRepository


class CarrinhoVazio(Exception):
    pass


class CupomInvalido(Exception):
    pass


class PedidoService:
    def __init__(self, pedido_repo=None, livro_repo=None):
        self._pedido_repo = pedido_repo or PedidoRepository()
        self._livro_repo = livro_repo or LivroRepository()

    def montar_calculo(self, carrinho, codigo_cupom=None):
    
        calculo = PrecoBaseCarrinho(carrinho)
        calculo = DescontoProgressivo(calculo, carrinho.quantidade_total())

        if codigo_cupom:
            percentual = percentual_do_cupom(codigo_cupom)
            if percentual is None:
                raise CupomInvalido(f"Cupom '{codigo_cupom}' invalido.")
            calculo = CupomDesconto(calculo, codigo_cupom.strip().upper(), percentual)

        calculo = Imposto(calculo)
        calculo = Frete(calculo)
        return calculo

    def finalizar_pedido(self, usuario_id, carrinho, codigo_cupom=None):
        if carrinho.esta_vazio():
            raise CarrinhoVazio("Carrinho vazio.")

        calculo = self.montar_calculo(carrinho, codigo_cupom)
        total = round(calculo.calcular(), 2)

        # Valida estoque:
        itens_validados = []
        for item in carrinho.itens:
            livro = self._livro_repo.buscar_por_id(item.livro.id)
            if livro is None:
                raise ValueError(f"Livro nao encontrado: {item.livro.titulo}")
            if not livro.tem_estoque_para(item.quantidade):
                raise ValueError(f"Estoque insuficiente: {livro.titulo}")
            itens_validados.append((livro, item.quantidade))

        
        pedido = Pedido(
            usuario_id=usuario_id,
            total=total,
            data=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self._pedido_repo.inserir(pedido)  # preenche pedido.id in-place
        pedido_id = pedido.id

        for livro, quantidade in itens_validados:
            livro.baixar_estoque(quantidade)
            self._livro_repo.atualizar(livro)
            self._pedido_repo.inserir_item(ItemPedido(
                livro_id=livro.id,
                quantidade=quantidade,
                preco_unitario=livro.preco,
                pedido_id=pedido_id,
            ))

        
        carrinho.limpar()
        return pedido_id

    def listar_pedidos_do_usuario(self, usuario_id):
        return self._pedido_repo.listar_por_usuario(usuario_id)

    def itens_do_pedido(self, pedido_id):
        return self._pedido_repo.listar_itens_detalhado(pedido_id)
