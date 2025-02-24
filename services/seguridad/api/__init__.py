import os
import threading
from flask import Flask, app, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import seguridad.modulos.anonimizacion.aplicacion
    import seguridad.modulos.hippa.aplicacion

def importar_modelos_alchemy():
    import seguridad.modulos.anonimizacion.infraestructura.dto
    import seguridad.modulos.hippa.infraestructura.dto

def comenzar_consumidor(app):
    import seguridad.modulos.anonimizacion.infraestructura.consumidores as anonimizacion
    import seguridad.modulos.hippa.infraestructura.consumidores as hippa


    # Suscripción a eventos
    threading.Thread(target=anonimizacion.suscribirse_a_eventos).start()
    threading.Thread(target=hippa.suscribirse_a_eventos).start()
    '''
    def wrap_app_context_eventos(modulo):
        def wrapper():
            with app.app_context():
                modulo.suscribirse_a_eventos()
        return wrapper
    def wrap_app_context_comandos(modulo):
            def wrapper():
                with app.app_context():
                    modulo.suscribirse_a_comandos()
            return wrapper
    # Suscripción a eventos
    threading.Thread(target=wrap_app_context_eventos(anonimizacion)).start()
    threading.Thread(target=wrap_app_context_eventos(hippa)).start()

    '''
    # Suscripción a comandos dentro del contexto de la app
    def suscribir_comandos():
        with app.app_context():  # Asegurar contexto de Flask
            anonimizacion.suscribirse_a_comandos()
            hippa.suscribirse_a_comandos()
    
    threading.Thread(target=suscribir_comandos).start()

def create_app(configuracion={}):
    # Init la aplicación de Flask
    app = Flask(__name__, instance_relative_config=True)

    # Configuración de BD
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

    # Inicializa la DB
    from seguridad.config.db import init_db
    init_db(app)

    from seguridad.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
        db.create_all()

        if not app.config.get('TESTING'):
            print('comenzar_consumidor()')
            comenzar_consumidor(app)  # Pasamos la app para el contexto

    # Importa Blueprints
    from . import anonimizaciones, hippa

    # Registro de Blueprints
    app.register_blueprint(anonimizaciones.bp)
    app.register_blueprint(hippa.bp)

    @app.route("/spec", methods=["GET"])
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "anonimizacion de los Andes"
        return jsonify(swag)

    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "up"}

    app.logger.setLevel(logging.DEBUG)
    return app
