import seguridad.seedwork.presentacion.api as api
import json
from flask import redirect, render_template, request, session, url_for
from flask import Response

from seguridad.seedwork.dominio.excepciones import ExcepcionDominio
from seguridad.modulos.anonimizacion.aplicacion.mapeadores import MapeadorAnonimizacionDTOJson
from seguridad.modulos.anonimizacion.aplicacion.servicios import ServicioAnonimizacion
from seguridad.modulos.anonimizacion.aplicacion.queries.obtener_anonimizacion import ObtenerAnonimizacion
from seguridad.modulos.anonimizacion.aplicacion.comandos.crear_anonimizacion import CrearAnonimizacion
from seguridad.seedwork.aplicacion.queries import ejecutar_query
from seguridad.modulos.anonimizacion.infraestructura.despachadores import Despachador

bp = api.crear_blueprint('anonimizacion', '/anonimizacion')

@bp.route('/anonimizacion', methods=['POST'])
def agregar_anonimizacion():
    try:
        anonimizacion_dict = request.json
        map_anonimizacion = MapeadorAnonimizacionDTOJson()
        anonimizacion_dto = map_anonimizacion.externo_a_dto(anonimizacion_dict)
        comando = CrearAnonimizacion(anonimizacion_dto.fecha_creacion, anonimizacion_dto.fecha_actualizacion, anonimizacion_dto.id, anonimizacion_dto.nombre, anonimizacion_dto.imagen, anonimizacion_dto.fecha_fin)
        despachador = Despachador()
        despachador.publicar_comando(comando, 'public/default/comandos-anonimizacion')
        
        return Response('{anonimizacion realizada}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/error_anonimizacion', methods=['POST'])
def agregar_error_anonimizacion():    
    from seguridad.modulos.anonimizacion.infraestructura.schema.v1.eventos import ErrorAnonimizacion
    try:
        data = request.json
        usuario = data["imagen"]
        comando = ErrorAnonimizacion(usuario)
        despachador = Despachador()
        despachador.publicar_comando_error(comando, 'public/default/comandos-error_anonimizacion')
        return Response('{Error Usuario}', status=202, mimetype='application/json')
    
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/anonimizacion', methods=['GET'])
@bp.route('/anonimizacion/<id>', methods=['GET'])
def dar_anonimizacion(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerAnonimizacion(id))
        map_anonimizacion = MapeadorAnonimizacionDTOJson()
        return map_anonimizacion.dto_a_externo(query_resultado.resultado)
    
    else:
        sr = ServicioAnonimizacion()
        return sr.obtener_todas_las_anonimizacion()
    