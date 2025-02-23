from pydispatch import dispatcher
from .handlers import HandlerHippaIntegracion
from seguridad.modulos.hippa.dominio.eventos import ValidacionHippaCancelada, ValidacionHippaCreada, ValidacionHippaFinalizada, ValidacionHippaIniciada

dispatcher.connect(HandlerHippaIntegracion.handle_hippa_creada,
                   signal=f'{ValidacionHippaCreada.__name__}Integracion')
dispatcher.connect(HandlerHippaIntegracion.handle_hippa_iniciada,
                   signal=f'{ValidacionHippaIniciada.__name__}Integracion')
dispatcher.connect(HandlerHippaIntegracion.handle_hippa_cancelada,
                   signal=f'{ValidacionHippaCancelada.__name__}Integracion')
dispatcher.connect(HandlerHippaIntegracion.handle_hippa_finalizada,
                   signal=f'{ValidacionHippaFinalizada.__name__}Integracion')
