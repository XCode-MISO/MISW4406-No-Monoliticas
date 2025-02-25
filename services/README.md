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

## Escenario de calidad

Se va a probar el escenario de calidad: Procesamiento de 30,000 centrod de datos de salud, para el atributo de escalidad.
Se implementó un patrón de microservicio, con una arquitectura orientada a eventos y comunicación asíncrona. 
Esto se hizo utilizando apache pulsar como plataforma de mensajería distribuida y se utilizó para comunicar los módulos de anonimización y validación hippa.
Cuando se crea una anonimización, y esta se escribe exitosaemente en la base de datos, se crea un evento de integración de comando para activar el
modulo de validación de reglas hippa.

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
