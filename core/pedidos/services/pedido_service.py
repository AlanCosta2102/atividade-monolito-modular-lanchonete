from core.pedidos.repositories.pedido_repository import PedidoRepository

class PedidoService:

    def __init__(self):
        self.repository = PedidoRepository()

    def buscar(self, pedido_id):
        return self.repository.buscar(pedido_id)

    def preparar(self, pedido_id):

        pedido = self.buscar(pedido_id)

        pedido.status = "PREPARANDO"

        self.repository.salvar(pedido)

        return pedido