from django.db import transaction

from core.pagamento.repositories.pagamento_repository import (
    PagamentoRepository
)

from core.pagamento.gateways.mock_gateway import (
    MockGateway
)

from core.pedidos.api.pedido_api import (
    PedidoAPI
)

from core.notificacao.api.notificacao_api import (
    NotificacaoAPI
)

class PagamentoService:

    def __init__(self):

        self.repository = PagamentoRepository()

        self.gateway = MockGateway()

    @transaction.atomic
    def processar(self, transacao_id):

        transacao = self.repository.buscar(
            transacao_id
        )

        resposta = self.gateway.processar()

        transacao.status = resposta["status"]

        self.repository.salvar(
            transacao
        )

        if transacao.status == "APPROVED":

            pedido = PedidoAPI.buscar(
                transacao.pedido.id
            )

            PedidoAPI.preparar(
                pedido.id
            )

            NotificacaoAPI.enviar(
                pedido
            )

        return transacao