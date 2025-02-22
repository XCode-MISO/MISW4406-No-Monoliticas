from pydispatch import dispatcher




from .handlers import HandlerAnonimizacionIntegracion




from pda.modulos.anonimizacion.dominio.eventos import AnonimizacionCreada, AnonimizacionIniciada, AnonimizacionCancelada, AnonimizacionFinalizada








dispatcher.connect(HandlerAnonimizacionIntegracion.handle_reserva_creada, signal=f'{AnonimizacionCreada.__name__}Integracion')



dispatcher.connect(HandlerAnonimizacionIntegracion.handle_reserva_cancelada, signal=f'{AnonimizacionIniciada.__name__}Integracion')



dispatcher.connect(HandlerAnonimizacionIntegracion.handle_reserva_pagada, signal=f'{AnonimizacionFinalizada.__name__}Integracion')




dispatcher.connect(HandlerAnonimizacionIntegracion.handle_reserva_aprobada, signal=f'{AnonimizacionCancelada.__name__}Integracion')