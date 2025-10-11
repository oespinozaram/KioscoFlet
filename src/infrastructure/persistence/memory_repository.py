# src/infrastructure/persistence/memory_repository.py
from src.domain.pedido import Pedido
from src.application.repositories import PedidoRepository

class PedidoRepositoryEnMemoria(PedidoRepository):
    _pedido_actual: Pedido | None = None

    def guardar(self, pedido: Pedido):
        self._pedido_actual = pedido

    def obtener(self) -> Pedido:
        if self._pedido_actual is None:
            self._pedido_actual = Pedido()
        return self._pedido_actual
