# src/domain/datos_entrega.py
from dataclasses import dataclass

@dataclass
class DatosEntrega:
    nombre_completo: str = ""
    telefono: str = ""
    direccion: str = ""
    numero_exterior: str = ""
    entre_calles: str = ""
    codigo_postal: str = ""
    colonia: str = ""
    ciudad: str = ""
    municipio: str = ""
    estado: str = ""
    referencias: str = ""
