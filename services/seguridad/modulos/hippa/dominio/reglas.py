"""Reglas de negocio del dominio de anonimizaciones

En este archivo usted encontrará reglas de negocio del dominio de anonimizaciones

"""

from seguridad.seedwork.dominio.reglas import ReglaNegocio
from .entidades import Imagen


class NormativaPrivacidadPago(ReglaNegocio):
    imagen: Imagen
    
    def __init__(self, imagen, mensaje='no tiene información en la imagen relacionada con el pago.'):
        super().__init__(mensaje)
        self.imagen = imagen

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_de_pago()

class NormativaPrivacidadProveedorSanitario(ReglaNegocio):
    imagen: Imagen
    
    def __init__(self, imagen, mensaje='no tiene información en la imagen relacionada con el proveedor sanitario.'):
        super().__init__(mensaje)
        self.imagen = imagen

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_del_proveedor_sanitario()

class NormativaPrivacidadFisica(ReglaNegocio):
    imagen: Imagen
    
    def __init__(self, imagen, mensaje='no tiene información en la imagen relacionada con el físico del paciente.'):
        super().__init__(mensaje)
        self.imagen = imagen

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_fisica()

class NormativaPrivacidadMental(ReglaNegocio):
    imagen: Imagen
    
    def __init__(self, imagen, mensaje='no tiene información en la imagen relacionada con el estado mental del paciente.'):
        super().__init__(mensaje)
        self.imagen = imagen

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_mental()

class NormativaPrivacidadPersonal(ReglaNegocio):
    imagen: Imagen
    
    def __init__(self, imagen, mensaje='no tiene información en la imagen persional del paciente'):
        super().__init__(mensaje)
        self.imagen = imagen

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_personal()

class NormativaPrivacidadSanitaria(ReglaNegocio):
    imagen: Imagen
    
    def __init__(self, imagen, mensaje='no tiene información en la imagen relacionada con la institucion de salud'):
        super().__init__(mensaje)
        self.imagen = imagen

    def es_valido() -> bool:
        return not Imagen.tiene_informacion_sanitaria()