from pydispatch import dispatcher
from .handlers import HandlerAnonimizacionIntegracion
from seguridad.modulos.anonimizacion.dominio.eventos import AnonimizacionCreada, AnonimizacionIniciada, AnonimizacionCancelada, AnonimizacionFinalizada

dispatcher.connect(HandlerAnonimizacionIntegracion.handle_anonimizacion_creada,
                   signal=f'{AnonimizacionCreada.__name__}Integracion')
dispatcher.connect(HandlerAnonimizacionIntegracion.handle_anonimizacion_iniciada,
                   signal=f'{AnonimizacionIniciada.__name__}Integracion')
dispatcher.connect(HandlerAnonimizacionIntegracion.handle_anonimizacion_finalizada,
                   signal=f'{AnonimizacionFinalizada.__name__}Integracion')
dispatcher.connect(HandlerAnonimizacionIntegracion.handle_anonimizacion_cancelada,
                   signal=f'{AnonimizacionCancelada.__name__}Integracion')
