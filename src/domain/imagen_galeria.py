# src/domain/imagen_galeria.py
from typing import NamedTuple

class ImagenGaleria(NamedTuple):
    id: int
    url: str
    descripcion: str
    categoria: str | None
    tags: str | None
