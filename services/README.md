# Diseño y Construcción de Soluciones No Monoliticas

## Grupo: XCode
### Integrantes:
| Nombre                        | Correo                                                            |
| ----------------------------- | ----------------------------------------------------------------- |
|Andres Losada|af.losada@uniandes.edu.co|
|Esneider Restrepo|erestrepoe@uniandes.edu.co|
|Emerson Chaparro|echaparroa@uniandes.edu.co|
|Cristian Arias|ca.ariasv1@uniandes.edu.co|

## Entrega 3

## Ejecutar aplicación:

 - Activar ambiente virtual:

    venv\Scripts\activate

 - Instalar dependencia: 

    pip install -r requirements.txt

 - Ejecutar Servidor Seguridad Http en modo debug:

    flask --app seguridad/api --debug run
    
 - Para ejecutar el docker-compose hacer lo siguiente

 ```bash
docker build . -f seguridad.Dockerfile -t seguridad/flask
docker compose up -d
 ```
