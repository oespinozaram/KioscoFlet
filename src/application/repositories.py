# src/application/repositories.py
from abc import ABC, abstractmethod
from typing import NamedTuple
from src.domain.pedido import Pedido
from src.domain.imagen_galeria import ImagenGaleria


class Categoria(NamedTuple):
    id: int
    nombre: str
    imagen_url: str


class TipoPan(NamedTuple):
    id: int
    nombre: str
    imagen_url: str


class FormaPastel(NamedTuple):
    nombre: str
    imagen_url: str


class TipoRelleno(NamedTuple):
    nombre: str
    imagen_url: str


class TipoCobertura(NamedTuple):
    nombre: str
    imagen_url: str


class CategoriaRepository(ABC):
    @abstractmethod
    def obtener_todas(self) -> list[Categoria]:
        pass


class PedidoRepository(ABC):
    @abstractmethod
    def guardar(self, pedido: Pedido):
        pass

    @abstractmethod
    def obtener(self) -> Pedido:
        pass


class TamanoRepository(ABC):
    @abstractmethod
    def obtener_todos(self) -> list[str]:
        pass


class TipoPanRepository(ABC):
    @abstractmethod
    def obtener_por_categoria(self, id_categoria: int) -> list[TipoPan]:
        pass


class TipoFormaRepository(ABC):
    @abstractmethod
    def obtener_por_categoria(self, id_categoria: int) -> list[FormaPastel]:
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


class Ticket(NamedTuple):
    id_pedido: int
    id_categoria: int
    fecha_creacion: str
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


class FinalizarPedidoRepository(ABC):
    @abstractmethod
    def guardar(self, pedido: Pedido) -> int:
        pass

    @abstractmethod
    def obtener_por_id(self, id_pedido: int) -> Ticket | None:
        pass