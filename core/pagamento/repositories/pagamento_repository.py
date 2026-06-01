from core.models import (
    TransacaoMock
)

class PagamentoRepository:

    def buscar(self, transacao_id):

        return (
            TransacaoMock.objects
            .select_for_update()
            .get(
                id_transacao=transacao_id
            )
        )

    def salvar(self, transacao):

        transacao.save()