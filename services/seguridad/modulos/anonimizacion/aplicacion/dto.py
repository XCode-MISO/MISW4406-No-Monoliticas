from dataclasses import dataclass, field
from seguridad.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class AnonimizacionDTO(DTO):
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
    fecha_fin: int = field(default_factory=int)
