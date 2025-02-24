import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
from flask import current_app


from seguridad.modulos.hippa.infraestructura.schema.v1.eventos import EventoValidacionHippaCreada
from seguridad.modulos.hippa.infraestructura.schema.v1.comandos import ComandoCrearValidacionHippa
from seguridad.seedwork.infraestructura import utils

from seguridad.modulos.hippa.aplicacion.mapeadores import MapeadorImagenHippaDTOJson
from seguridad.modulos.hippa.aplicacion.servicios import ServicioValidacionHippa

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('eventos-validacion_hippa', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='seguridad-sub-eventos', schema=AvroSchema(EventoValidacionHippaCreada))

        print("suscribirse_a_eventos()")
        while True:
            mensaje = consumidor.receive()
            print(f'Evento recibido: {mensaje.value().data}')

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
        consumidor = cliente.subscribe('comandos-validacion_hippa', 
                consumer_type=_pulsar.ConsumerType.Shared, 
                subscription_name='seguridad-sub-comandos', 
                schema=AvroSchema(ComandoCrearValidacionHippa)
            )     
        
        print("suscribirse_a_comandos()")

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')
            
            hippa_dict = mensaje.value().data.__dict__            
            map_validacion = MapeadorImagenHippaDTOJson()
            print('dto: {map_validacion}')
            validacion_dto = map_validacion.externo_a_dto(hippa_dict)
            sr = ServicioValidacionHippa()
            dto_final = sr.crear_validacion_hippa(validacion_dto)

            consumidor.acknowledge(mensaje)     
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()