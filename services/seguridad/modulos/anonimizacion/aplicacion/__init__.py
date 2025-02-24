from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from seguridad.modulos.anonimizacion.dominio.eventos import AnonimizacionAgregada 

dispatcher.connect(HandlerReservaIntegracion.handle_anonimizacion_agregada, signal=f'{AnonimizacionAgregada.__name__}Integracion')
