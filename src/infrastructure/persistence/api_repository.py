import requests
import sqlite3
from src.application.repositories import FinalizarPedidoRepository, Ticket
import logging

logger = logging.getLogger(__name__)


class FinalizarPedidoRepositoryAPI(FinalizarPedidoRepository):
    def __init__(self, api_url: str, db_path: str):
        self.api_url = api_url
        self.db_path = db_path

    def _obtener_id_sucursal(self) -> int:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nSucursalPK FROM Sucursales LIMIT 1")
                result = cursor.fetchone()
                return int(result[0]) if result and result[0] is not None else 1
        except sqlite3.Error as e:
            print(f"Error obteniendo ID de sucursal: {e}")
            return 1

    def guardar(self, pedido: Ticket) -> int:

        id_sucursal = self._obtener_id_sucursal()

        payload = {
            "id": pedido.id_pedido,
            "nSucursalPK": id_sucursal,
            "fecha_creacion": pedido.fecha_creacion or "",
            "fecha_entrega": pedido.fecha_entrega or "",
            "tamano_pastel": pedido.tamano_pastel or "",
            "id_categoria": pedido.id_categoria,
            "tipo_pan": pedido.tipo_pan or "",
            "tipo_forma": pedido.tipo_forma or "",
            "tipo_relleno": pedido.tipo_relleno or "",
            "tipo_cobertura": pedido.tipo_cobertura or "",
            "nombre_completo": pedido.nombre_cliente or "",
            "telefono": pedido.telefono_cliente or "",
            "direccion": pedido.direccion_cliente or "",
            "numero_exterior": pedido.num_ext_cliente or "",
            "entre_calles": pedido.entre_calles_cliente or "",
            "codigo_postal": pedido.cp_cliente or "",
            "colonia": pedido.colonia_cliente or "",
            "ciudad": pedido.ciudad_cliente or "",
            "municipio": pedido.municipio_cliente or "",
            "estado": pedido.estado_cliente or "",
            "referencias": pedido.referencias_cliente or "",
            "decorado_liso_color1": pedido.decorado_liso_color1 or "",
            "decorado_liso_color2": pedido.decorado_liso_color2 or "",
            "mensaje_pastel": pedido.mensaje_pastel or "",
            "extra_flor_cantidad": pedido.extra_flor_cantidad or 0,
            "hora_entrega": pedido.hora_entrega or "",
            "tipo_decorado": pedido.tipo_decorado or "",
            "decorado_liso_detalle": pedido.decorado_liso_detalle or "",
            "decorado_tematica_detalle": pedido.decorado_tematica_detalle or "",
            "decorado_imagen_id": pedido.decorado_imagen_id or 0,
            "extra_seleccionado": pedido.extra_seleccionado or "",
            "extra_costo": pedido.extra_costo or 0,
            "total": pedido.total or 0,
            "monto_deposito": pedido.monto_deposito or 0,
            "nombre_categoria": pedido.nombre_categoria or "",
            "tamano_descripcion": pedido.tamano_descripcion or "",
            "tamano_peso": pedido.tamano_peso or "",
            "edad_pastel": pedido.edad_pastel or "",
            "imagen_pastel": pedido.imagen_pastel or "",
        }

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()

            response_data = response.json()
            nuevo_id = response_data.get("id", 0)
            logger.info(f"INFO: Pedido enviado al web service. Nuevo ID: {nuevo_id}")
            return nuevo_id

        except requests.exceptions.RequestException as e:
            logger.error(f"ERROR: No se pudo enviar el pedido al web service: {e}")
            return 0

    def obtener_por_id(self, id_pedido: int) -> Ticket | None:
        return None
