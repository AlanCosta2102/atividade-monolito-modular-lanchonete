from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import views
from .views import health

router = DefaultRouter()

# Cardápio
router.register(
    r'itens',
    views.ItemViewSet,
    basename='item'
)

# Pagamento
router.register(
    r'formas-pagamento',
    views.FormaPagamentoViewSet,
    basename='formapagamento'
)

# Pedidos
router.register(
    r'pedidos',
    views.PedidoViewSet,
    basename='pedido'
)

# Notificações
router.register(
    r'notificacoes',
    views.NotificacaoCozinhaViewSet,
    basename='notificacao'
)

urlpatterns = [

    # Health Check
    path(
        'health/',
        health,
        name='health'
    ),

    # Rotas da API
    path(
        '',
        include(router.urls)
    ),
]