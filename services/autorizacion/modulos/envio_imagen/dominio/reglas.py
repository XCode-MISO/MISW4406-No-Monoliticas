"""Reglas de negocio del dominio de validacion_usuarioes

En este archivo usted encontrará reglas de negocio del dominio de validacion_usuarioes

"""

from autorizacion.seedwork.dominio.reglas import ReglaNegocio
from .entidades import Imagen


class NormativaPrivacidadPago(ReglaNegocio):
    image: Imagen
    
    def __init__(self, image, mensaje='no tiene información en la imagen relacionada con el pago.'):
        super().__init__(mensaje)
        self.image = image

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_de_pago()

class NormativaPrivacidadProveedorSanitario(ReglaNegocio):
    image: Imagen
    
    def __init__(self, image, mensaje='no tiene información en la imagen relacionada con el proveedor sanitario.'):
        super().__init__(mensaje)
        self.image = image

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_del_proveedor_sanitario()

class NormativaPrivacidadFisica(ReglaNegocio):
    image: Imagen
    
    def __init__(self, image, mensaje='no tiene información en la imagen relacionada con el físico del paciente.'):
        super().__init__(mensaje)
        self.image = image

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_fisica()

class NormativaPrivacidadMental(ReglaNegocio):
    image: Imagen
    
    def __init__(self, image, mensaje='no tiene información en la imagen relacionada con el estado mental del paciente.'):
        super().__init__(mensaje)
        self.image = image

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_mental()

class NormativaPrivacidadPersonal(ReglaNegocio):
    image: Imagen
    
    def __init__(self, image, mensaje='no tiene información en la imagen persional del paciente'):
        super().__init__(mensaje)
        self.image = image

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_personal()

class NormativaPrivacidadSanitaria(ReglaNegocio):
    image: Imagen
    
    def __init__(self, image, mensaje='no tiene información en la imagen relacionada con la institucion de salud'):
        super().__init__(mensaje)
        self.image = image

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_sanitaria()