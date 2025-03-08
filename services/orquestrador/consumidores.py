import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from ingestion_datos.utils import broker_host
from orquestrador.orquestrador import CoordinadorProcesamientoDatos
from seguridad.seedwork.aplicacion.sagas import CoordinadorOrquestacion

async def suscribirse_a_topico(
        topico: str, 
        suscripcion: str, 
        schema: Record, 
        tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared, 
        orquestrador: CoordinadorProcesamientoDatos = CoordinadorProcesamientoDatos()
        ):
    try:
        async with aiopulsar.connect(f'pulsar://{broker_host()}:6650') as cliente:
            async with cliente.subscribe(
                topico, 
                consumer_type=tipo_consumidor,
                subscription_name=suscripcion, 
                schema=AvroSchema(schema)
            ) as consumidor:
                while True:
                    mensaje = await consumidor.receive()
                    datos = mensaje.value()
                    print(f'Evento recibido: {datos}')
                    print(f'Tipo: {type(datos)}')
                    await orquestrador.oir_mensaje(mensaje=datos)
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error(f'ERROR: Suscribiendose al tópico! {topico}, {suscripcion}, {schema}')
        traceback.print_exc()