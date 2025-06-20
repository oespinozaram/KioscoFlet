# src/application/use_cases.py
import datetime
from .repositories import (
    PedidoRepository, TamanoRepository, CategoriaRepository,
    TipoPanRepository, TipoFormaRepository, TipoRellenoRepository,
    TipoCoberturaRepository, FinalizarPedidoRepository, Categoria, TipoPan
)
from src.domain.datos_entrega import DatosEntrega
from src.domain.pedido import Pedido
from src.infrastructure.services.qr_service import QRService


class PedidoUseCases:
    def __init__(self, pedido_repo: PedidoRepository, tamano_repo: TamanoRepository,
                 categoria_repo: CategoriaRepository, tipo_pan_repo: TipoPanRepository,
                 tipo_forma_repo: TipoFormaRepository, tipo_relleno_repo: TipoRellenoRepository,
                 tipo_cobertura_repo: TipoCoberturaRepository, finalizar_repo: FinalizarPedidoRepository,
                 qr_service: QRService):
        self.pedido_repo = pedido_repo
        self.tamano_repo = tamano_repo
        self.categoria_repo = categoria_repo
        self.tipo_pan_repo = tipo_pan_repo
        self.tipo_forma_repo = tipo_forma_repo
        self.tipo_relleno_repo = tipo_relleno_repo
        self.tipo_cobertura_repo = tipo_cobertura_repo
        self.finalizar_repo = finalizar_repo
        self.qr_service = qr_service
        self.tamanos_disponibles = []

    def obtener_coberturas_por_categoria(self, id_categoria: int) -> list[str]:
        return self.tipo_cobertura_repo.obtener_por_categoria(id_categoria)

    def seleccionar_tipo_cobertura(self, nombre_cobertura: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_cobertura = nombre_cobertura
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Cobertura '{nombre_cobertura}' seleccionada. Estado del pedido: {pedido}")

    def obtener_rellenos_disponibles(self, id_categoria: int, id_tipo_pan: int) -> list[str]:
        return self.tipo_relleno_repo.obtener_por_categoria_y_pan(id_categoria, id_tipo_pan)

    def seleccionar_tipo_relleno(self, nombre_relleno: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_relleno = nombre_relleno
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Relleno '{nombre_relleno}' seleccionado. Estado del pedido: {pedido}")

    def obtener_formas_por_categoria(self, id_categoria: int) -> list[str]:
        return self.tipo_forma_repo.obtener_por_categoria(id_categoria)

    def seleccionar_tipo_forma(self, nombre_forma: str):
        pedido = self.pedido_repo.obtener()
        pedido.tipo_forma = nombre_forma
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Forma '{nombre_forma}' seleccionada. Estado del pedido: {pedido}")

    def obtener_panes_por_categoria(self, id_categoria: int) -> list[TipoPan]:
        return self.tipo_pan_repo.obtener_por_categoria(id_categoria)

    def seleccionar_tipo_pan(self, nombre_pan: str):
        pedido = self.pedido_repo.obtener()
        if pedido.tipo_pan != nombre_pan:
            pedido.tipo_relleno = None
        pedido.tipo_pan = nombre_pan
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Pan '{nombre_pan}' seleccionado. Estado del pedido: {pedido}")

        pedido.tipo_pan = nombre_pan

        self.pedido_repo.guardar(pedido)
        print(f"INFO: Pan '{nombre_pan}' seleccionado. Estado del pedido: {pedido}")

    def obtener_categorias(self) -> list[Categoria]:
        return self.categoria_repo.obtener_todas()

    def seleccionar_categoria(self, id_categoria: int):
        pedido = self.pedido_repo.obtener()
        pedido.id_categoria = id_categoria
        pedido.tipo_pan = None
        pedido.tipo_forma = None
        pedido.tipo_relleno = None
        pedido.tipo_cobertura = None
        self.pedido_repo.guardar(pedido)
        print(f"INFO: Categoría {id_categoria} seleccionada. Estado del pedido: {pedido}")

    def seleccionar_fecha(self, fecha: datetime.date):
        pedido = self.pedido_repo.obtener()
        pedido.fecha_entrega = fecha
        self.pedido_repo.guardar(pedido)

    def reiniciar_fecha(self):
        pedido = self.pedido_repo.obtener()
        pedido.fecha_entrega = None
        self.pedido_repo.guardar(pedido)

    def obtener_pedido_actual(self):
        return self.pedido_repo.obtener()

    def obtener_tamanos(self) -> list[str]:
        if not self.tamanos_disponibles:
            self.tamanos_disponibles = self.tamano_repo.obtener_todos()

        # Seleccionar el primero por defecto si no hay ninguno
        pedido = self.pedido_repo.obtener()
        if not pedido.tamano_pastel and self.tamanos_disponibles:
            pedido.tamano_pastel = self.tamanos_disponibles[0]
            self.pedido_repo.guardar(pedido)

        return self.tamanos_disponibles

    def seleccionar_siguiente_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        if not tamanos or not pedido.tamano_pastel:
            return

        try:
            idx = tamanos.index(pedido.tamano_pastel)
            nuevo_idx = (idx + 1) % len(tamanos)
            pedido.tamano_pastel = tamanos[nuevo_idx]
            self.pedido_repo.guardar(pedido)
        except ValueError:
            # Si el tamaño actual no está en la lista, selecciona el primero
            pedido.tamano_pastel = tamanos[0]
            self.pedido_repo.guardar(pedido)

    def seleccionar_anterior_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        if not tamanos or not pedido.tamano_pastel:
            return

        try:
            idx = tamanos.index(pedido.tamano_pastel)
            nuevo_idx = (idx - 1 + len(tamanos)) % len(tamanos)
            pedido.tamano_pastel = tamanos[nuevo_idx]
            self.pedido_repo.guardar(pedido)
        except ValueError:
            pedido.tamano_pastel = tamanos[0]
            self.pedido_repo.guardar(pedido)

    def reiniciar_tamano(self):
        pedido = self.pedido_repo.obtener()
        tamanos = self.obtener_tamanos()
        pedido.tamano_pastel = tamanos[0] if tamanos else None
        self.pedido_repo.guardar(pedido)


    def guardar_datos_y_finalizar(self, datos: dict) -> tuple[Pedido, str]:
        """
        Guarda los datos de entrega, finaliza el pedido en la BD,
        genera un QR y devuelve el pedido y el string base64 del QR.
        """
        # 1. Guardar los datos en el objeto Pedido
        pedido = self.pedido_repo.obtener()
        pedido.datos_entrega = DatosEntrega(**datos)
        self.pedido_repo.guardar(pedido)

        # 2. Guardar permanentemente en la base de datos
        print("INFO: Finalizando pedido y guardando en la base de datos...")
        self.finalizar_repo.finalizar(pedido)
        print("INFO: ¡Pedido guardado permanentemente!")

        # 3. Preparar datos para el QR
        # (Omitimos datos sensibles o muy largos para que el QR no sea muy denso)
        datos_qr = (
            f"Cliente: {pedido.datos_entrega.nombre_completo}\n"
            f"Telefono: {pedido.datos_entrega.telefono}\n"
            f"Fecha Entrega: {pedido.fecha_entrega.strftime('%d/%m/%Y') if pedido.fecha_entrega else 'N/A'}\n"
            f"Tamaño: {pedido.tamano_pastel}\n"
            f"Forma: {pedido.tipo_forma}\n"
            f"Pan: {pedido.tipo_pan}"
        )

        # 4. Generar el QR usando el servicio
        qr_base64 = self.qr_service.generar_qr_base64(datos_qr)

        # 5. Devolver el pedido completo y el QR
        return pedido, qr_base64