from core.models import NotificacaoCozinha

class NotificacaoService:

    def enviar(self, pedido):

        return NotificacaoCozinha.objects.create(
            pedido=pedido
        )