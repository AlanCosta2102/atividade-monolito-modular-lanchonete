from core.notificacao.services.notificacao_service import (
    NotificacaoService
)

class NotificacaoAPI:

    @staticmethod
    def enviar(pedido):

        return (
            NotificacaoService()
            .enviar(
                pedido
            )
        )