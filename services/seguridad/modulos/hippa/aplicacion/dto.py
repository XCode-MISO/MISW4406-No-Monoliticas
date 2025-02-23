from dataclasses import dataclass, field
from aeroalpes.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class ImagenHippaDTO(DTO):

    id: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
    estado: str = field(default_factory=str)
