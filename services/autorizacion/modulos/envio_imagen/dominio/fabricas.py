""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import ValidacionEnvio_Imagen
from .reglas import NormativaPrivacidadFisica, NormativaPrivacidadMental, NormativaPrivacidadPago, NormativaPrivacidadPersonal, NormativaPrivacidadProveedorSanitario, NormativaPrivacidadSanitaria
from autorizacion.seedwork.dominio.repositorios import Mapeador, Repositorio
from autorizacion.seedwork.dominio.fabricas import Fabrica
from autorizacion.seedwork.dominio.entidades import Entidad
from autorizacion.modulos.envio_imagen.dominio.entidades import ValidacionEnvio_Imagen
from dataclasses import dataclass

import logging


@dataclass
class _FabricaValidacionEnvio_Imagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            envio_imagen: ValidacionEnvio_Imagen = mapeador.dto_a_entidad(obj)
            self.validar_regla(NormativaPrivacidadFisica)
            self.validar_regla(NormativaPrivacidadMental)
            self.validar_regla(NormativaPrivacidadPago)
            self.validar_regla(NormativaPrivacidadPersonal)
            self.validar_regla(NormativaPrivacidadProveedorSanitario)
            self.validar_regla(NormativaPrivacidadSanitaria)
            return envio_imagen

@dataclass
class FabricaValidacionEnvio_Imagen(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == ValidacionEnvio_Imagen.__class__:
            fabrica_validacion = _FabricaValidacionEnvio_Imagen()
            return fabrica_validacion.crear_objeto(obj, mapeador)
        else:
            raise Exception()
