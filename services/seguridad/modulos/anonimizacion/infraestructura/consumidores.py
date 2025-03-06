import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json
from datetime import datetime

from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregada
from seguridad.modulos.anonimizacion.infraestructura.schema.v1.comandos import ComandoCrearAnonimizacion
from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacionDTOJson
from seguridad.modulos.anonimizacion.aplicacion.servicios import ServicioAnonimizacion
from seguridad.modulos.anonimizacion.aplicacion.comandos.crear_anonimizacion import CrearAnonimizacion
from seguridad.seedwork.infraestructura import utils

from seguridad.seedwork.aplicacion.comandos import ejecutar_commando


from seguridad.modulos.hippa.infraestructura.despachadores import Despachador
from seguridad.modulos.hippa.aplicacion.comandos.crear_validacion_hippa import CrearValidacionHippa

def suscribirse_a_eventos():
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('public/default/eventos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='seguridad-sub-eventos', schema=AvroSchema(AnonimizacionAgregada))

        print("suscribirse_a_eventos_ingestion()")
        while True:
            mensaje = consumidor.receive()
#########################################
            print(f'Evento recibido: {mensaje.value().data}')
#########################################
            try:
                consumidor.acknowledge(mensaje)
            except:
                pass

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
        #consumidor = cliente.subscribe('comandos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='aeroalpes-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))
        consumidor = cliente.subscribe('public/default/comandos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='seguridad-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))
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
            # try:
            #     consumidor.acknowledge(mensaje)
            # except:
            #     pass
            # from seguridad.modulos.hippa.infraestructura.despachadores import Despachador
            # from seguridad.modulos.hippa.aplicacion.comandos.crear_validacion_hippa import CrearValidacionHippa
            # from seguridad.modulos.hippa.aplicacion.mapeadores import MapeadorImagenHippaDTOJson
            # from seguridad.modulos.hippa.aplicacion.servicios import ServicioValidacionHippa

            # x_dict = {'estado': None, 'image': dto_final.imagen, 'id': dto_final.id, 'fecha_creacion': dto_final.fecha_creacion, 'fecha_actualizacion': dto_final.fecha_actualizacion}
            # x_map = MapeadorImagenHippaDTOJson()
            # x_dto = x_map.externo_a_dto(x_dict)            
            # x_comando = CrearValidacionHippa(    
            #     id=f'{uuid.uuid4()}',        
            #     image=anonimizacion_dto.imagen
            # ,   fecha_creacion=datetime.now().strftime(_FORMATO_FECHA)
            # ,   fecha_actualizacion=datetime.now().strftime(_FORMATO_FECHA)
            # ,   estado=None
            # )
            # x_despachador = Despachador()
            # x_despachador.publicar_comando(x_comando, 'public/default/comandos-validacion_hippa')
            
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()