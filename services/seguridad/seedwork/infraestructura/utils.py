import time
import os
import datetime
import requests
from fastavro.schema import parse_schema
from pulsar.schema import *

epoch = datetime.datetime.utcfromtimestamp(0)
PULSAR_ENV: str = 'BROKER_HOST'
FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

def time_millis():
    return int(time.time() * 1000)

def broker_host():
    return os.getenv('BROKER_HOST', default='127.0.0.1')

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def datetime_a_str(date):
    return date.strftime(FORMATO_FECHA)

def str_date_time(date: str):
    return datetime.datetime.strptime(date, FORMATO_FECHA)

def broker_host():
    return os.getenv(PULSAR_ENV, default="localhost")

def consultar_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    return json.loads(json_registry.get('data',{}))

def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)