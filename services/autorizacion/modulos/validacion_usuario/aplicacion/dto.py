from dataclasses import dataclass, field
from autorizacion.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class Validacion_UsuarioDTO(DTO):
    fecha_actualizacion: str = field(default_factory=str)
    fecha_validacion: str = field(default_factory=str)
    id: str = field(default_factory=str)
    usuario: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    imagen: str = field(default_factory=str)
    fecha_fin: str = field(default_factory=str)
