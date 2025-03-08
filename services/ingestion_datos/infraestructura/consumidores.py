import datetime
import logging
import traceback
import uuid
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
                    print(f'Evento recibido en ingestion_datos con data: {datos.data}')

                    if type(datos) == ComandoIngerirDatos:
                        # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
                        execute_transaction_projection(
                            TotalIngestionDatosProjection(
                                datos.time,
                                TotalIngestionDatosProjection.ADD
                            )
                        )
                        if (datos.data.imagen == "maligno"):
                            from ingestion_datos.infraestructura.despachadores import Despachador as DespechadorIngestion
                            despachador = DespechadorIngestion()
                            payload = IngestionCancelada(
                                id = datos.id,
                                id_correlacion = datos.data.id_correlacion,
                                ingestion_id = datos.id,
                                fecha_actualizacion = utils.datetime_a_str(datetime.datetime.now())
                            )
                            evento = EventoIngestion(
                                ingestion_cancelada=payload,
                                datacontenttype="IngestionCancelada"
                            )
                            despachador.publicar_mensaje(evento, 'public/default/evento-ingestion-datos')
                            await consumidor.acknowledge(mensaje)
                            continue
                        from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador
                        from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import AnonimizacionAgregadaPayload
                        despachador = Despachador()
                        datosComando = datos.data
                        print(f"Ingestion datos: {datosComando}")
                        evento = AnonimizacionAgregadaPayload(
                                id_anonimizacion=str(uuid.uuid4()),
                                estado="Iniciado",
                                fecha_creacion=utils.time_millis(),
                                fecha_evento=datetime.datetime.now(),
                                nombre=datosComando.nombre,
                                imagen=datosComando.imagen
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

                    elif type(datos) == ComandoRevertirIngestionDatos:
                        # TODO Identificar el tipo de CRUD del evento: Creacion, actualización o eliminación.
                        execute_transaction_projection(
                            TotalIngestionDatosProjection(
                                datos.time,
                                TotalIngestionDatosProjection.DELETE
                            )
                        )
                        coreografiaError(datos)

                    await consumidor.acknowledge(mensaje)

    except:
        logging.error(
            f'ERROR: Suscribiendose al tópico! {topico}, {suscripcion}, {schema}')
        traceback.print_exc()

def coreografiaError(datos):
    from autorizacion.modulos.validacion_usuario.infraestructura.despachadores import Despachador
    from autorizacion.modulos.validacion_usuario.infraestructura.schema.v1.eventos import ErrorValidacion_Usuario, ErrorValidacion_UsuarioPayload
    despachador = Despachador()
    payload = ErrorValidacion_UsuarioPayload(
        nombre=datos.data.id_correlacion
    )
    evento = ErrorValidacion_Usuario(
        data = payload
    )
    despachador.pub_mensaje_error(evento, 'public/default/evento-error-validacion-usuario')
    print(f"Coordinacion mediante evento error validacion-usuario publicado {evento}")