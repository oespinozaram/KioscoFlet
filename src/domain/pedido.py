# src/domain/pedido.py
import datetime
from .datos_entrega import DatosEntrega

class Pedido:
    """Entidad que representa el estado de un pedido de pastel."""
    def __init__(self):
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

    def reiniciar(self):
        """Reinicia la entidad a su estado por defecto."""
        self.fecha_entrega = None
        self.hora_entrega = None
        self.tamano_pastel = None
        self.id_categoria = None
        self.tipo_pan = None
        self.tipo_forma = None
        self.tipo_relleno = None
        self.tipo_cobertura = None
        self.datos_entrega = None
        self.mensaje_pastel = None
        self.tipo_decorado = None
        self.decorado_liso_detalle = None
        self.decorado_tematica_detalle = None
        self.decorado_imagen_id = None
        self.extra_seleccionado = None
        self.decorado_liso_color = None

    def __str__(self):
        return f"Pedido(Categoria: {self.id_categoria}, Decorado: '{self.tipo_decorado}', Mensaje: '{self.mensaje_pastel}')"