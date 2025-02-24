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
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        #consumidor = cliente.subscribe('comandos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))
        consumidor = cliente.subscribe('comandos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='seguridad-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))
#########################################        
        print("suscribirse_a_comandos()")
#########################################

        while True:
            mensaje = consumidor.receive()
            print(f'================> Comando recibido: {mensaje.value().data}')
########################################
            anonimizacion_dict = mensaje.value().data.__dict__            
            map_anonimizacion = MapeadorAnonimizacionDTOJson()
            anonimizacion_dto = map_anonimizacion.externo_a_dto(anonimizacion_dict)
            sr = ServicioAnonimizacion()
            dto_final = sr.crear_anonimizacion(anonimizacion_dto)
########################################
            consumidor.acknowledge(mensaje)
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()