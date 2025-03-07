import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import json
from datetime import datetime

from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregada, AnonimizacionAgregadaPayload
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
        consumidor = cliente.subscribe('public/default/eventos-anonimizacion-finalizada', consumer_type=_pulsar.ConsumerType.Shared,subscription_name='seguridad-sub-eventos', schema=AvroSchema(AnonimizacionAgregada))

        print("suscribirse_a_eventos()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n================> Evento recibido: {mensaje.value().data}')
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
        consumidor = cliente.subscribe('public/default/comandos-anonimizacion', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='seguridad-sub-comandos', schema=AvroSchema(ComandoCrearAnonimizacion))
        print("suscribirse_a_comandos()")
        while True:
            mensaje = consumidor.receive()
            print(f'\n================> Comando recibido: {mensaje.value().data}')
            anonimizacion_dict = mensaje.value().data.__dict__            
            map_anonimizacion = MapeadorAnonimizacionDTOJson()
            anonimizacion_dto = map_anonimizacion.externo_a_dto(anonimizacion_dict)            
            sr = ServicioAnonimizacion()
            dto_final = sr.crear_anonimizacion(anonimizacion_dto)
            consumidor.acknowledge(mensaje)
            despacharEventoAnonimizacionFinalizada(anonimizacion_dto)           
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def despacharEventoAnonimizacionFinalizada(dto_final):
    from datetime import datetime
    from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador
    print("\n=================> parametro dto: ", dto_final)
    evento = AnonimizacionAgregadaPayload(
        id_anonimizacion="12345",
        estado="COMPLETADO",
        fecha_creacion=datetime.utcnow().isoformat()
    )
    print("\n=================> evento: ", evento)
    despachador = Despachador()
    despachador.publicar_evento(evento, 'public/default/eventos-anonimizacion-finalizada')
    print("\n=================> Evento despachado!!!!!!!!!")