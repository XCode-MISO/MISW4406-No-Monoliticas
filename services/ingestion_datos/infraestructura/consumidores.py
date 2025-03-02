import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from seguridad.seedwork.infraestructura import utils
from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador
from ingestion_datos.infraestructura.proyecciones import execute_transaction_projection, IngestionDatosAnalitica, TotalIngestionDatosProjection

async def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared):
    try:
        async with aiopulsar.connect(f'pulsar://{utils.broker_host()}:6650') as cliente:
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

                    # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
                    execute_transaction_projection(
                        TotalIngestionDatosProjection(
                                datos.time, 
                                TotalIngestionDatosProjection.ADD
                            )
                        )
                    
                    despachador = Despachador()
                    await consumidor.acknowledge(mensaje)    

    except:
        logging.error(f'ERROR: Suscribiendose al tópico! {topico}, {suscripcion}, {schema}')
        traceback.print_exc()