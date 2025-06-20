# src/domain/pedido.py
import datetime
from .datos_entrega import DatosEntrega

class Pedido:
    """Entidad que representa el estado de un pedido de pastel."""
    def __init__(self):
        self.fecha_entrega: datetime.date | None = None
        self.tamano_pastel: str | None = None
        self.id_categoria: int | None = None
        self.tipo_pan: str | None = None
        self.tipo_forma: str | None = None
        self.tipo_relleno: str | None = None
        self.tipo_cobertura: str | None = None
        self.datos_entrega: DatosEntrega | None = None

    def reiniciar(self):
        """Reinicia la entidad a su estado por defecto."""
        self.fecha_entrega = None
        self.tamano_pastel = None
        self.id_categoria = None
        self.tipo_pan = None
        self.tipo_forma = None
        self.tipo_relleno = None
        self.tipo_cobertura = None
        self.datos_entrega = None

    def __str__(self):
        return (f"Pedido(Categoria: {self.id_categoria}, Fecha: {self.fecha_entrega}, "
                f"Tamaño: '{self.tamano_pastel}', Pan: '{self.tipo_pan}', "
                f"Forma: '{self.tipo_forma}', Relleno: '{self.tipo_relleno}', "
                f"Cobertura: '{self.tipo_cobertura}')")