from src.application.repositories import FinalizarPedidoRepository, Ticket
from src.domain.pedido import Pedido
import logging

logger = logging.getLogger(__name__)

class FinalizarPedidoRepositoryComposite(FinalizarPedidoRepository):
    def __init__(self, sqlite_repo: FinalizarPedidoRepository, api_repo: FinalizarPedidoRepository):
        self.sqlite_repo = sqlite_repo
        self.api_repo = api_repo

    def guardar(self, pedido: Pedido) -> int:
        id_pedido_local = self.sqlite_repo.guardar(pedido)

        if id_pedido_local == 0:
            return 0

        ticket_completo = self.sqlite_repo.obtener_por_id(id_pedido_local)

        if not ticket_completo:
            logger.error("ERROR: No se pudo recuperar el pedido local para enviarlo a la API.")
            return id_pedido_local

        try:
            id_api = self.api_repo.guardar(ticket_completo)
            if id_api > 0:
                logger.error(f"INFO: Pedido {id_pedido_local} sincronizado con el web service.")
            else:
                logger.warning("ADVERTENCIA: Pedido no se pudo sincronizar con el web service.")
        except Exception as e:
            logger.warning(f"ADVERTENCIA: Error al sincronizar con la API: {e}")

        return id_pedido_local

    def obtener_por_id(self, id_pedido: int) -> Ticket | None:
        return self.sqlite_repo.obtener_por_id(id_pedido)
