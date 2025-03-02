import time
import os
import datetime
import requests
import json
from fastavro.schema import parse_schema
from pulsar.schema import *

PULSAR_ENV: str = 'BROKER_HOST'

def sta_host():
    return os.getenv("PDA_ENV", default="localhost")

def sta_port():
    return os.getenv("PDA_PORT", default="5001")

def broker_host():
    return os.getenv("PULSAR_ENV", default="localhost")

def get_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    return json.loads(json.dumps(json_registry.get('data',{})))

def get_schema_avro_from_dict(json_schema: dict) -> AvroSchema:
    schema_definition = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=schema_definition)