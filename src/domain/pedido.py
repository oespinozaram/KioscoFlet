# src/domain/pedido.py
import datetime
from .datos_entrega import DatosEntrega

class Pedido:
    def __init__(self):
        self.id_pedido: int | None = None
        self.fecha_creacion: str | None = None
        self.fecha_entrega: datetime.date | None = None
        self.hora_entrega: str | None = None
        self.tamano_pastel: str | None = None
        self.id_categoria: int | None = None
        self.tipo_pan: str | None = None
        self.tipo_forma: str | None = None
        self.tipo_relleno: str | None = None
        self.tipo_cobertura: str | None = None
        self.datos_entrega: DatosEntrega | None = None
        self.mensaje_pastel: str | None = None
        self.tipo_decorado: str | None = None
        self.decorado_liso_detalle: str | None = None
        self.decorado_tematica_detalle: str | None = None
        self.decorado_imagen_id: int | None = None
        self.decorado_liso_color: str | None = None
        self.extra_seleccionado: str | None = None
        self.decorado_liso_color1: str | None = None
        self.decorado_liso_color2: str | None = None
        self.extra_flor_cantidad: int | None = None
        self.descrip_tamano: str | None = None
        self.id_tamano: int | None = None
        self.id_forma: int | None = None
        self.id_pan: int | None = None
        self.extra_precio: float | None = None
        self.precio_pastel: float | None = None
        self.total: float | None = None
        self.monto_deposito: float | None = None
        self.nombre_categoria: str | None = None
        self.tamano_peso: str | None = None
        self.tamano_descripcion: str | None = None
        self.imagen_pastel: str | None = None
        self.edad_pastel: int | None = None
        self.precio_chocolate: float | None = None
        self.incluye: str | None = None

    def reiniciar(self):
        self.id_pedido: int | None = None
        self.fecha_creacion: str | None = None
        self.fecha_entrega: datetime.date | None = None
        self.hora_entrega: str | None = None
        self.tamano_pastel: str | None = None
        self.id_categoria: int | None = None
        self.tipo_forma: str | None = None
        self.tipo_pan: str | None = None
        self.tipo_relleno: str | None = None
        self.tipo_cobertura: str | None = None
        self.tipo_decorado: str | None = None
        self.decorado_liso_detalle: str | None = None
        self.decorado_tematica_detalle: str | None = None
        self.decorado_imagen_id: int | None = None
        self.decorado_liso_color1: str | None = None
        self.decorado_liso_color2: str | None = None
        self.mensaje_pastel: str | None = None
        self.extra_seleccionado: str | None = None
        self.extra_flor_cantidad: int | None = None
        self.nombre_cliente: str | None = None
        self.telefono_cliente: str | None = None
        self.direccion_cliente: str | None = None
        self.num_ext_cliente: str | None = None
        self.entre_calles_cliente: str | None = None
        self.cp_cliente: str | None = None
        self.colonia_cliente: str | None = None
        self.ciudad_cliente: str | None = None
        self.municipio_cliente: str | None = None
        self.estado_cliente: str | None = None
        self.referencias_cliente: str | None = None
        self.id_tamano: int | None = None
        self.id_forma: int | None = None
        self.id_pan: int | None = None
        self.descrip_tamano: str | None = None
        self.extra_precio: float | None = None
        self.precio_pastel: float | None = None
        self.total: float | None = None
        self.monto_deposito: float | None = None
        self.nombre_categoria: str | None = None
        self.tamano_peso: str | None = None
        self.tamano_descripcion: str | None = None
        self.imagen_pastel: str | None = None
        self.edad_pastel: int | None = None
        self.precio_chocolate: float | None = None
        self.incluye: str | None = None

    def __str__(self):
        return f"Pedido(Categoria: {self.id_categoria}, Decorado: '{self.tipo_decorado}', Mensaje: '{self.mensaje_pastel}')"