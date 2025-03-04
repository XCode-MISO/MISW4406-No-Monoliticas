import autorizacion.seedwork.presentacion.api as api
from datetime import datetime
import json
from flask import redirect, render_template, request, session, url_for, jsonify
from flask import Response

from autorizacion.seedwork.dominio.excepciones import ExcepcionDominio
from autorizacion.modulos.envio_imagen.aplicacion.mapeadores import MapeadorImagenEnvio_ImagenDTOJson
from autorizacion.modulos.envio_imagen.aplicacion.servicios import ServicioValidacionEnvio_Imagen
from autorizacion.modulos.envio_imagen.dominio.objetos_valor import Status
from autorizacion.modulos.envio_imagen.aplicacion.queries.obtener_validacion_envio_imagen import ObtenerValidacionEnvio_Imagen
from autorizacion.modulos.envio_imagen.aplicacion.comandos.crear_validacion_envio_imagen import CrearValidacionEnvio_Imagen
from autorizacion.seedwork.aplicacion.queries import ejecutar_query
from autorizacion.modulos.envio_imagen.infraestructura.despachadores import Despachador


bp = api.crear_blueprint('envio_imagen', '/envio_imagen')
_FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

@bp.route('/validacion-envio_imagen', methods=['POST'])
def agregar_validacion_envio_imagen():
    try:
        validacion_envio_imagen_dict = request.json
        map_validacion_envio_imagen = MapeadorImagenEnvio_ImagenDTOJson()
        validacion_envio_imagen_dto = map_validacion_envio_imagen.externo_a_dto(validacion_envio_imagen_dict)
        comando = CrearValidacionEnvio_Imagen(
            id=validacion_envio_imagen_dto.id
        ,   image=validacion_envio_imagen_dto.imagen
        ,   fecha_validacion=datetime.now().strftime(_FORMATO_FECHA)
        ,   fecha_actualizacion=datetime.now().strftime(_FORMATO_FECHA)
        ,   estado=None
        )
        despachador = Despachador()
        print("""comando: ({comando})""".format(comando=comando))
        despachador.publicar_comando(comando, 'comandos-validacion_envio_imagen')
        
        return Response(
                json.dumps(dict(
                    id=comando.id, 
                    image=comando.image, 
                    fecha_validacion=str(comando.fecha_validacion), 
                    fecha_actualizacion=str(comando.fecha_actualizacion)
                )), 
                status=202, 
                mimetype='application/json'
            )
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')

@bp.route('/validacion-envio_imagen', methods=['GET'])
@bp.route('/validacion-envio_imagen/<id>', methods=['GET'])
def dar_validacion_envio_imagen(id=None):
    if id:
        query_resultado = ejecutar_query(ObtenerValidacionEnvio_Imagen(id))
        map_validacion_envio_imagen = MapeadorImagenEnvio_ImagenDTOJson()
        return map_validacion_envio_imagen.dto_a_externo(query_resultado.resultado)
    else:
        sr = ServicioValidacionEnvio_Imagen()
        return sr.obtener_validacion_envio_imagen_por_id(id)
    