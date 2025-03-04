from pydispatch import dispatcher

from .handlers import HandlerReservaIntegracion

from autorizacion.modulos.validacion_usuario.dominio.eventos import Validacion_UsuarioAgregada 

dispatcher.connect(HandlerReservaIntegracion.handle_validacion_usuario_agregada, signal=f'{Validacion_UsuarioAgregada.__name__}Integracion')
