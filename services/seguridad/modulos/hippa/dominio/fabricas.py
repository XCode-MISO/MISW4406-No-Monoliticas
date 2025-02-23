""" Fábricas para la creación de objetos del dominio de vuelos

En este archivo usted encontrará las diferentes fábricas para crear
objetos complejos del dominio de vuelos

"""

from .entidades import Reserva
from .reglas import NormativaPrivacidadFisica, NormativaPrivacidadMental, NormativaPrivacidadPago, NormativaPrivacidadPersonal, NormativaPrivacidadProveedorSanitario, NormativaPrivacidadSanitaria
from .excepciones import TipoObjetoNoExisteEnDominioVuelosExcepcion
from seguridad.seedwork.dominio.repositorios import Mapeador, Repositorio
from seguridad.seedwork.dominio.fabricas import Fabrica
from seguridad.seedwork.dominio.entidades import Entidad
from seguridad.modulos.hippa.dominio.entidades import ValidacionHippa
from dataclasses import dataclass


@dataclass
class _FabricaValidacionHippa(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if isinstance(obj, Entidad):
            return mapeador.entidad_a_dto(obj)
        else:
            hippa: ValidacionHippa = mapeador.dto_a_entidad(obj)
            self.validar_regla(NormativaPrivacidadFisica)
            self.validar_regla(NormativaPrivacidadMental)
            self.validar_regla(NormativaPrivacidadPago)
            self.validar_regla(NormativaPrivacidadPersonal)
            self.validar_regla(NormativaPrivacidadProveedorSanitario)
            self.validar_regla(NormativaPrivacidadSanitaria)
            return hippa

@dataclass
class FabricaValidacionHippa(Fabrica):
    def crear_objeto(self, obj: any, mapeador: Mapeador) -> any:
        if mapeador.obtener_tipo() == Reserva.__class__:
            fabrica_validacion = _FabricaValidacionHippa()
            return fabrica_validacion.crear_objeto(obj, mapeador)
        else:
            raise Exception()
