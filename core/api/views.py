from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import (
    Item,
    Pedido,
    FormaPagamento,
    TransacaoMock,
    NotificacaoCozinha
)

from .serializers import (
    ItemSerializer,
    PedidoSerializer,
    NotificacaoCozinhaSerializer,
    FormaPagamentoSerializer
)

from core.pagamento.services.pagamento_service import (
    PagamentoService
)


class ItemViewSet(viewsets.ModelViewSet):
    """
    CRUD do Cardápio
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class FormaPagamentoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lista as formas de pagamento disponíveis
    """
    queryset = FormaPagamento.objects.filter(ativo=True)
    serializer_class = FormaPagamentoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    """
    Criação e Listagem de Pedidos
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = self.request.user

        if usuario.is_staff:
            return Pedido.objects.all()

        return Pedido.objects.filter(cliente=usuario)

    @action(detail=True, methods=['post'])
    def pagar(self, request, pk=None):

        pedido = self.get_object()

        # Pedido precisa estar aguardando pagamento
        if pedido.status != 'CRIADO':
            return Response(
                {
                    "erro": "Este pedido já foi pago ou não está disponível para pagamento."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        forma_pagamento_id = request.data.get(
            'forma_pagamento_id'
        )

        if not forma_pagamento_id:
            return Response(
                {
                    "erro": "A forma de pagamento é obrigatória."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            forma_pagamento = FormaPagamento.objects.get(
                id=forma_pagamento_id
            )

        except FormaPagamento.DoesNotExist:

            return Response(
                {
                    "erro": "Forma de pagamento inválida."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cria a transação
        transacao = TransacaoMock.objects.create(
            pedido=pedido,
            valor=pedido.get_total(),
            forma_pagamento=forma_pagamento
        )

        # Chama o módulo de pagamento
        transacao_processada = (
            PagamentoService()
            .processar(
                transacao.id_transacao
            )
        )

        if transacao_processada.status == 'APPROVED':

            return Response(
                {
                    "mensagem": "Pagamento aprovado! A cozinha já foi notificada."
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "erro": "Pagamento recusado."
            },
            status=status.HTTP_402_PAYMENT_REQUIRED
        )


class NotificacaoCozinhaViewSet(viewsets.ModelViewSet):
    """
    Visualização das notificações da cozinha
    """
    queryset = (
        NotificacaoCozinha.objects
        .all()
        .order_by('-criado_em')
    )

    serializer_class = (
        NotificacaoCozinhaSerializer
    )

    @action(detail=True, methods=['post'])
    def marcar_lida(self, request, pk=None):

        notificacao = self.get_object()

        notificacao.lida = True

        notificacao.save()

        return Response(
            {
                "mensagem": "Notificação marcada como lida."
            }
        )