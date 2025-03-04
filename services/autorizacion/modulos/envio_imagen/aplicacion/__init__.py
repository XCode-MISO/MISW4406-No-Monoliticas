from pydispatch import dispatcher
from .handlers import HandlerEnvio_ImagenIntegracion
from autorizacion.modulos.envio_imagen.dominio.eventos import ValidacionEnvio_ImagenCancelada, ValidacionEnvio_ImagenCreada, ValidacionEnvio_ImagenFinalizada, ValidacionEnvio_ImagenIniciada

dispatcher.connect(HandlerEnvio_ImagenIntegracion.handle_envio_imagen_creada,
                   signal=f'{ValidacionEnvio_ImagenCreada.__name__}Integracion')
dispatcher.connect(HandlerEnvio_ImagenIntegracion.handle_envio_imagen_iniciada,
                   signal=f'{ValidacionEnvio_ImagenIniciada.__name__}Integracion')
dispatcher.connect(HandlerEnvio_ImagenIntegracion.handle_envio_imagen_cancelada,
                   signal=f'{ValidacionEnvio_ImagenCancelada.__name__}Integracion')
dispatcher.connect(HandlerEnvio_ImagenIntegracion.handle_envio_imagen_finalizada,
                   signal=f'{ValidacionEnvio_ImagenFinalizada.__name__}Integracion')
