from core.pedidos.services.pedido_service import PedidoService

class PedidoAPI:

    @staticmethod
    def buscar(pedido_id):
        return PedidoService().buscar(
            pedido_id
        )

    @staticmethod
    def preparar(pedido_id):
        return PedidoService().preparar(
            pedido_id
        )