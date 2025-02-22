from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class AnonimizacionDTO(DTO):

    id: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    fecha_fin: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
