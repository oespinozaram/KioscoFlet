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
        """Busca una única imagen por su ID primario."""
        pass


class TipoColorRepository(ABC):
    @abstractmethod
    def obtener_por_categoria_y_cobertura(self, id_categoria: int, nombre_cobertura: str) -> list[str]:
        pass


class Ticket(NamedTuple):
    id_pedido: int
    nombre_cliente: str


class FinalizarPedidoRepository(ABC):
    @abstractmethod
    def finalizar(self, pedido: Pedido) -> int:
        pass

    @abstractmethod
    def obtener_por_id(self, id_pedido: int) -> Ticket | None:
        pass