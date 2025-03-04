import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json
from datetime import datetime

from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import Validacion_UsuarioAgregada
from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.comandos import ComandoCrearValidacion_Usuario
from autorizacion.seedwork.infraestructura import utils

from autorizacion.modulos.validacion_usuario.aplicacion.mapeadores import MapeadorValidacion_UsuarioDTOJson
from autorizacion.modulos.validacion_usuario.aplicacion.servicios import ServicioValidacion_Usuario

from autorizacion.modulos.envio_imagen.infraestructura.despachadores import Despachador
from autorizacion.modulos.envio_imagen.aplicacion.comandos.crear_validacion_envio_imagen import CrearValidacionEnvio_Imagen

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-validacion_usuario', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='autorizacion-sub-eventos', schema=AvroSchema(Validacion_UsuarioAgregada))

        print("suscribirse_a_eventos()")
        while True:
            mensaje = consumidor.receive()
#########################################
            print(f'Evento recibido: {mensaje.value().data}')
#########################################
            consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de eventos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_comandos():
    
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        #consumidor = cliente.subscribe('comandos-validacion_usuario', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearValidacion_Usuario))
        consumidor = cliente.subscribe('comandos-validacion_usuario', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='autorizacion-sub-comandos', schema=AvroSchema(ComandoCrearValidacion_Usuario))
#########################################        
        print("suscribirse_a_comandos()")
#########################################

        while True:
            mensaje = consumidor.receive()
            print(f'================> Comando recibido: {mensaje.value().data}')
########################################
            validacion_usuario_dict = mensaje.value().data.__dict__            
            map_validacion_usuario = MapeadorValidacion_UsuarioDTOJson()
            validacion_usuario_dto = map_validacion_usuario.externo_a_dto(validacion_usuario_dict)
            sr = ServicioValidacion_Usuario()
            dto_final = sr.crear_validacion_usuario(validacion_usuario_dto)
########################################
            consumidor.acknowledge(mensaje)
            from autorizacion.modulos.envio_imagen.infraestructura.despachadores import Despachador
            from autorizacion.modulos.envio_imagen.aplicacion.comandos.crear_validacion_envio_imagen import CrearValidacionEnvio_Imagen
            from autorizacion.modulos.envio_imagen.aplicacion.mapeadores import MapeadorImagenEnvio_ImagenDTOJson
            from autorizacion.modulos.envio_imagen.aplicacion.servicios import ServicioValidacionEnvio_Imagen

            x_dict = {'estado': None, 'image': dto_final.imagen, 'id': dto_final.id, 'fecha_validacion': dto_final.fecha_validacion, 'fecha_actualizacion': dto_final.fecha_actualizacion}
            x_map = MapeadorImagenEnvio_ImagenDTOJson()
            x_dto = x_map.externo_a_dto(x_dict)            
            x_comando = CrearValidacionEnvio_Imagen(    
                id=f'{uuid.uuid4()}',        
                image=validacion_usuario_dto.imagen
            ,   fecha_validacion=datetime.now().strftime(_FORMATO_FECHA)
            ,   fecha_actualizacion=datetime.now().strftime(_FORMATO_FECHA)
            ,   estado=None
            )
            x_despachador = Despachador()
            x_despachador.publicar_comando(x_comando, 'comandos-validacion_envio_imagen')
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()