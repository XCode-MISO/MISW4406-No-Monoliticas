import logging
import traceback
import pulsar, _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from ingestion_datos.utils import broker_host, datetime_a_str, millis_a_datetime, time_millis
from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador
from ingestion_datos.infraestructura.proyecciones import execute_transaction_projection, TotalIngestionDatosProjection
from ingestion_datos.dominio.eventos import IngestionFinalizada, EventoIngestion
from ingestion_datos.infraestructura.despachadores import Despachador as DespachadorIngestion

async def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared):
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

async def suscribirse_a_evento_usuario_valido(topico: str, suscripcion: str, schema: Record, tipo_consumidor:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared):
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
                    payload = IngestionFinalizada(
                        id = datos.id,
                        id_correlacion = datos.id_correlacion,
                        ingestion_id = datos.ingestion_id,
                        imagen = datos.imagen,
                        nombre = datos.nombre,
                        fecha_creacion = datetime_a_str(millis_a_datetime(time_millis()))
                    )
                    evento = EventoIngestion(
                         time=time_millis(),
                         ingestion=time_millis(),
                         datacontenttype=IngestionFinalizada.__name__,
                         ingestion_finalizada = payload
                    )
                    print(f"PAYLOAD: {payload.__dict__}")
                    despachador = DespachadorIngestion()
                    despachador.publicar_mensaje(evento, "public/default/evento-ingestion-datos")
    except:
        logging.error(f'ERROR: Suscribiendose al tópico! {topico}, {suscripcion}, {schema}')
        traceback.print_exc()