from dataclasses import dataclass, field
from autorizacion.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class ImagenEnvio_ImagenDTO(DTO):
    id: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
    estado: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    fecha_validacion: str = field(default_factory=str)