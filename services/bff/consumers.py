import logging
import traceback
import pulsar, _pulsar
import aiopulsar
from pulsar.schema import *
from . import util

async def suscribe_to_topic(topic: str, suscription: str, schema: str, consumer_type:_pulsar.ConsumerType=_pulsar.ConsumerType.Shared, events=[]):
    try:
        json_schema = util.get_schema_registry(schema)
        avro_schema = util.get_schema_avro_from_dict(json_schema)
        async with aiopulsar.connect(f'pulsar://{util.broker_host()}:6650') as client:
            async with client.subscribe(
                topic,
                consumer_type=consumer_type,
                subscription_name=suscription,
                schema=avro_schema
            ) as consumer:
                while True:
                    message = await consumer.receive()
                    data = message.value()
                    print(f'oo=======> EVENTO: {data}')
                    events.append(str(data))
                    await consumer.acknowledge(message)

    except:
        logging.error(f'ERROR: no se pudo suscribir a topico: {topic}, {suscription}, {schema}')
        traceback.print_exc()