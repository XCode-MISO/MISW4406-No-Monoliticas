import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json

from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregada
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion
from seguridad.seedwork.infraestructura import utils

from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacionDTOJson
from seguridad.modulos.anonimizacion.aplicacion.servicios import ServicioAnonimizacion

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='seguridad-sub-eventos', schema=AvroSchema(AnonimizacionAgregada))

        print("oo-------> anonimizacion_suscribirse_a_eventos()")
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
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        #consumidor = cliente.subscribe('comandos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))
        consumidor = cliente.subscribe('comandos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='seguridad-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))
#########################################        
        print("oo-------> anonimizacion_suscribirse_a_comandos()")
#########################################

        while True:
            mensaje = consumidor.receive()
            print(f'oo-------> anonimizacion:  Comando recibido: {mensaje.value().data}')
########################################
            anonimizacion_dict = mensaje.value().data.__dict__            
            map_anonimizacion = MapeadorAnonimizacionDTOJson()
            anonimizacion_dto = map_anonimizacion.externo_a_dto(anonimizacion_dict)
            sr = ServicioAnonimizacion()
            dto_final = sr.crear_anonimizacion(anonimizacion_dto)

            from seguridad.modulos.hippa.infraestructura.despachadores import Despachador
            from seguridad.modulos.hippa.aplicacion.comandos.crear_validacion_hippa import CrearValidacionHippa
            from seguridad.modulos.hippa.aplicacion.mapeadores import MapeadorImagenHippaDTOJson
            from seguridad.modulos.hippa.aplicacion.servicios import ServicioValidacionHippa
            
            x_dict = {'estado': 'NOMBRE-3', 'image': 'image', 'id': '1234567890', 'fecha_creacion': '2025-12-12', 'fecha_actualizacion': '2025-12-12'}
            x_map = MapeadorImagenHippaDTOJson()
            x_dto = x_map.externo_a_dto(x_dict)
            x_comando = CrearValidacionHippa(x_dto.id, x_dto.imagen, x_dto.estado, x_dto.fecha_creacion, x_dto.fecha_actualizacion)
            x_despachador = Despachador()
            x_despachador.publicar_comando(x_comando, 'comandos-hippa')
########################################
            consumidor.acknowledge(mensaje)
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()