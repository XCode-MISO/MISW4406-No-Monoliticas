import datetime
import logging
import traceback
import pulsar
import _pulsar
import aiopulsar
import asyncio
from pulsar.schema import *
from ingestion_datos.utils import broker_host, datetime_a_str, millis_a_datetime, time_millis
from ingestion_datos.infraestructura.proyecciones import execute_transaction_projection, TotalIngestionDatosProjection
from ingestion_datos.dominio.eventos import IngestionCancelada, IngestionFinalizada, EventoIngestion
from ingestion_datos.infraestructura.despachadores import Despachador as DespachadorIngestion
from ingestion_datos.aplicacion.comandos import ComandoIngerirDatos, ComandoRevertirIngestionDatos
from ingestion_datos import utils


async def suscribirse_a_topico(topico: str, suscripcion: str, schema: Record, tipo_consumidor: _pulsar.ConsumerType = _pulsar.ConsumerType.Shared):
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
                    print(f'Evento recibido en ingestion_datos: {datos}')

                    if type(datos) == ComandoIngerirDatos:
                        # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
                        execute_transaction_projection(
                            TotalIngestionDatosProjection(
                                datos.time,
                                TotalIngestionDatosProjection.ADD
                            )
                        )
                        from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador
                        from seguridad.modulos.anonimizacion.dominio.eventos import AnonimizacionAgregada
                        despachador = Despachador()
                        evento = AnonimizacionAgregada(
                                id=datos.id,
                                estado="Iniciado",
                                fecha_creacion=datetime.datetime.now(),
                                fecha_evento=datetime.datetime.now(),
                                id_cliente=datos.id,
                                id_reserva=datos.id
                            )
                        despachador.publicar_evento(evento, 'public/default/eventos-anonimizacion')
                        print(f"Evento de ingestion datos publicado {evento}")
                        """ despachador = DespachadorIngestion()
                        despachador.publicar_evento(
                            IngestionCancelada(
                                id=datos.id,
                                id_correlacion=datos.id_correllacion,
                                ingestion_id=datos.id,
                                fecha_actualizacion=utils.datetime_a_str(
                                    datetime.datetime.now()),
                            )) """

                    elif type(schema) == ComandoRevertirIngestionDatos:
                        # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
                        execute_transaction_projection(
                            TotalIngestionDatosProjection(
                                datos.time,
                                TotalIngestionDatosProjection.DELETE
                            )
                        )
                        

                    await consumidor.acknowledge(mensaje)

    except:
        logging.error(
            f'ERROR: Suscribiendose al tópico! {topico}, {suscripcion}, {schema}')
        traceback.print_exc()
