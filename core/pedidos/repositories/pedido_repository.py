from core.models import Pedido

class PedidoRepository:

    def buscar(self, pedido_id):
        return Pedido.objects.get(id=pedido_id)

    def listar(self):
        return Pedido.objects.all()

    def salvar(self, pedido):
        pedido.save()