# src/application/repositories.py
from abc import ABC, abstractmethod
from typing import NamedTuple
from src.domain.pedido import Pedido
from src.domain.imagen_galeria import ImagenGaleria


class Categoria(NamedTuple):
    id: int
    nombre: str

class TipoPan(NamedTuple):
    id: int
    nombre: str


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
    def obtener_por_categoria(self, id_categoria: int) -> list[str]:
        pass


class TipoRellenoRepository(ABC):
    @abstractmethod
    def obtener_por_categoria_y_pan(self, id_categoria: int, id_tipo_pan: int) -> list[str]:
        pass


class TipoCoberturaRepository(ABC):
    @abstractmethod
    def obtener_por_categoria_y_pan(self, id_categoria: int, id_tipo_pan: int) -> list[str]:
       pass

class FinalizarPedidoRepository(ABC):
    @abstractmethod
    def finalizar(self, pedido: Pedido):
        pass


class ImagenGaleriaRepository(ABC):
    @abstractmethod
    def obtener_todas(self) -> list[ImagenGaleria]:
        pass
