from core.models import NotificacaoCozinha


class NotificacaoRepository:

    @staticmethod
    def criar(pedido):
        return NotificacaoCozinha.objects.create(
            pedido=pedido
        )