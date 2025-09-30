# src/application/repositories.py
from abc import ABC, abstractmethod
from typing import NamedTuple
from src.domain.pedido import Pedido
from src.domain.imagen_galeria import ImagenGaleria
import datetime


class Categoria(NamedTuple):
    id: int
    nombre: str
    imagen_url: str


class TipoPan(NamedTuple):
    id: int
    nombre: str
    imagen_url: str


class FormaPastel(NamedTuple):
    id: int
    nombre: str
    imagen_url: str


class TipoRelleno(NamedTuple):
    nombre: str
    imagen_url: str


class TipoCobertura(NamedTuple):
    nombre: str
    imagen_url: str


class TamanoPastel(NamedTuple):
    id: int
    nombre: str
    descripcion: str
    peso: str


class Extra(NamedTuple):
    id: int
    descripcion: str
    costo: float

class ExtraRepository(ABC):
    @abstractmethod
    def obtener_por_descripcion(self, descripcion: str) -> Extra | None:
        pass


class CategoriaRepository(ABC):
    @abstractmethod
    def obtener_todas(self) -> list[Categoria]:
        pass

    @abstractmethod
    def obtener_por_id(self, id_categoria: int) -> Categoria | None:
        pass


class PedidoRepository(ABC):
    @abstractmethod
    def guardar(self, pedido: Pedido):
        pass

    @abstractmethod
    def obtener(self) -> Pedido:
        pass


class TipoPanRepository(ABC):
    @abstractmethod
    def obtener_por_categoria(self, id_categoria: int) -> list[TipoPan]:
        pass


class TipoRellenoRepository(ABC):
    @abstractmethod
    def obtener_por_categoria_y_pan(self, id_categoria: int, id_tipo_pan: int) -> list[TipoRelleno]:
        pass


class TipoCoberturaRepository(ABC):
    @abstractmethod
    def obtener_por_categoria_y_pan(self, id_categoria: int, id_tipo_pan: int) -> list[TipoCobertura]:
       pass


class ImagenGaleriaRepository(ABC):
    @abstractmethod
    def buscar(self, categoria: str | None = None, termino: str | None = None) -> list[ImagenGaleria]:
        pass

    @abstractmethod
    def obtener_por_id(self, id_imagen: int) -> ImagenGaleria | None:
        pass


class TipoColorRepository(ABC):
    @abstractmethod
    def obtener_por_categoria_y_cobertura(self, id_categoria: int, nombre_cobertura: str) -> list[str]:
        pass

class Horario(NamedTuple):
    hora_inicio: datetime.time
    hora_fin: datetime.time

class HorarioEntregaRepository(ABC):
    @abstractmethod
    def obtener_horario(self) -> Horario | None:
        pass

class DiaFestivoRepository(ABC):
    @abstractmethod
    def es_festivo(self, fecha: datetime.date) -> bool:
        pass


class Ticket(NamedTuple):
    id_pedido: int
    id_categoria: int
    fecha_creacion: str
    nombre_categoria: str
    tipo_pan: str
    tipo_forma: str
    tipo_relleno: str
    tipo_cobertura: str
    tamano_pastel: str
    fecha_entrega: str
    hora_entrega: str
    nombre_cliente: str
    telefono_cliente: str
    direccion_cliente: str
    num_ext_cliente: str
    entre_calles_cliente: str
    colonia_cliente: str
    ciudad_cliente: str
    municipio_cliente: str
    estado_cliente: str
    cp_cliente: str
    referencias_cliente: str
    decorado_liso_color: str
    decorado_liso_color1: str
    decorado_liso_color2: str
    mensaje_pastel: str
    hora_entrega: str
    extra_flor_cantidad: int
    tipo_decorado: str
    decorado_liso_detalle: str
    decorado_tematica_detalle: str
    decorado_imagen_id: int
    extra_seleccionado: str
    extra_costo: float
    precio_pastel: float
    monto_deposito: float
    total: float


class FinalizarPedidoRepository(ABC):
    @abstractmethod
    def guardar(self, pedido: Pedido) -> int:
        pass

    @abstractmethod
    def obtener_por_id(self, id_pedido: int) -> Ticket | None:
        pass


class TipoFormaRepository(ABC):
    @abstractmethod
    def obtener_por_categoria(self, id_categoria: int) -> list[FormaPastel]: # <-- Devuelve objeto
        pass


class TamanoRepository(ABC):
    @abstractmethod
    def obtener_todos(self) -> list[TamanoPastel]: # <-- Devuelve objeto
        pass


class PastelConfigurado(NamedTuple):
    precio_final: float
    monto_deposito: float


class PastelConfiguradoRepository(ABC):
    @abstractmethod
    def obtener_configuracion(self, id_cat: int, id_pan: int, id_forma: int, id_tam: int) -> PastelConfigurado | None:
        pass
