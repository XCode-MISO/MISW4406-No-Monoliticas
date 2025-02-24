import seguridad.seedwork.presentacion.api as api
from datetime import datetime
import json
from flask import redirect, render_template, request, session, url_for, jsonify
from flask import Response

from seguridad.seedwork.dominio.excepciones import ExcepcionDominio
from seguridad.modulos.hippa.aplicacion.mapeadores import MapeadorImagenHippaDTOJson
from seguridad.modulos.hippa.aplicacion.servicios import ServicioValidacionHippa
from seguridad.modulos.hippa.aplicacion.queries.obtener_validacion_hippa import ObtenerValidacionHippa
from seguridad.modulos.hippa.aplicacion.comandos.crear_validacion_hippa import CrearValidacionHippa
from seguridad.seedwork.aplicacion.queries import ejecutar_query
from seguridad.modulos.hippa.infraestructura.despachadores import Despachador


bp = api.crear_blueprint('hippa', '/hippa')


@bp.route('/validacion-hippa', methods=['POST'])
def agregar_validacion_hippa():
    try:
        validacion_hippa_dict = request.json
        map_validacion_hippa = MapeadorImagenHippaDTOJson()
        validacion_hippa_dto = map_validacion_hippa.externo_a_dto(validacion_hippa_dict)
        comando = CrearValidacionHippa(
            id=validacion_hippa_dto.id
        ,   image=validacion_hippa_dto.imagen
        ,   fecha_creacion=datetime.now()
        ,   fecha_actualizacion=datetime.now()
        )
        despachador = Despachador()
        print("""comando: ({comando})""".format(comando=comando))
        despachador.publicar_comando(comando, 'comandos-validacion_hippa')
        
        return Response(
                json.dumps(dict(
                    id=comando.id, 
                    image=comando.image, 
                    fecha_creacion=str(comando.fecha_creacion), 
                    fecha_actualizacion=str(comando.fecha_actualizacion)
                )), 
                status=202, 
                mimetype='application/json'
            )
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/validacion-hippa', methods=['GET'])
@bp.route('/validacion-hippa/<id>', methods=['GET'])
def dar_validacion_hippa(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerValidacionHippa(id))
        map_validacion_hippa = MapeadorImagenHippaDTOJson()
        return map_validacion_hippa.dto_a_externo(query_resultado.resultado)
    else:
        sr = ServicioValidacionHippa()
        return sr.obtener_validacion_hippa_por_id(id)
    