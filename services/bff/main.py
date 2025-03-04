from fastapi import FastAPI, Request
import asyncio
import traceback
import requests
import json


from pydantic import BaseSettings
from typing import Any

from .consumers import suscribe_to_topic

from . import util

class Config(BaseSettings):
    APP_VERSION: str = "1"

settings = Config()
app_configs: dict[str, Any] = {"title": "BFF SALUD-TECH-ALPES"}

app = FastAPI(**app_configs)
tasks = list()
events = list()

# @app.on_event("startup")
# async def app_startup():
#     global tasks
#     global events
#     task1 = asyncio.ensure_future(suscribe_to_topic("transaction-event", "sta-bff", "public/default/transaction-events", events=events))
#     tasks.append(task1)

# @app.on_event("shutdown")
# def shutdown_event():
#     global tasks
#     for task in tasks:
#         task.cancel()

@app.post('/v1/sta/transaction')
async def create_transaction(request: Request):
    try:
        transaction_data = await request.json()
        response_json = requests.post(f'http://{util.sta_host()}:{util.sta_port()}/validacion_usuario/validacion_usuario', json=transaction_data)
        if response_json.status_code != 202:
            return {"status": "error", "message": "Error al crear la transaccion"}
        return {"status": "ok", "message": "Transaccion creada"}
    except Exception as e:
        traceback.print_exc()
        return {"status": "error", "message": "An error occurred while creating the transaction"}


