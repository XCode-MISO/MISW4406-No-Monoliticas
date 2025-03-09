# Diseño y Construcción de Soluciones No Monoliticas

## Nombre del Equipo
XCODE

## Integrantes:
| Nombre | correo | Usuario |
|-|-|-|
| Andres Losada | af.losada@uniandes.edu.co | [AfLosada](https://github.com/AfLosada) |
| Cristian Arias | ca.ariasv1@uniandes.edu.co | [CristianAAV](https://github.com/CristianAAV) |
| Emerson Chaparro | e.chaparroa@uniandes.edu.co | [echaparroa-uniandes](https://github.com/echaparroa-uniandes) |
| Esneider Restrepo | e.restrepoe@uniandes.edu.co | [EsneiderRE](https://github.com/EsneiderRE) |

# Entrega 05
## Escenarios de calidad a probar
- 1: Escenario de calidad: Escalabilidad en la Integración con Sistemas de información de los data partners​
- 3: Escenario de calidad: Procesamiento de 30,000 centros de datos de salud​
- 4: Escenario de calidad: Disponibilidad del API de Autenticación​

## Distribucion del trabajo
| Nombre            | Tarea                     |
|-------------------|----------------------------|
| Andres Losada     | Orquestrador |
| Andres Losada     | Eventos de compensacion del Modulo de Ingestion |
| Andres Losada     | Despliegue GCP |
| Cristian Arias    | Adecuacion de servicios para la comunicacion con el orquestador |
| Cristian Arias    | Pruebas de cada enpoint, coleccion en postman |
| Emerson Chaparro  | Eventos de compensacion se servicio de seguridad |	
| Emerson Chaparro  | Eventos de compensacion se servicio de autorizacion |
| Esneider Restrepo | Refactorizacion de comandos y Eventos |	
| Esneider Restrepo | Eventos de compensacion se servicio de autorizacion |

## Estructura del proyecto
Para esta entrega se implementaron los siguientes archivos y carpetas:
- *services/autorizacion:* Servicio para la autorizacion de usuario
- *services/bff:* Implementacion del backend for frontend
- *services/ingestion_datos:* Servicio para la ingestion de archivos e imagenes
- *services/orquestrador:* Servicio de orquestracion
- *services/pulsar:* Archivos necesarios para desplegar pulsar en GCP
- *services/seguridad:* Servicion de seguridad de la entrega 1, contiene los modulos de anonimizacion e HIPPA
- *README.md:* Descripcion a instrucciones del proyecto
- *[archivo].Dockerfile:* Archivos necesarios para construir las imagenes utilizadas en el despliegue local o en nube
- *docker-compose.yml:* Orquesta y gestiona los contenedores.
- *requirements.txt:* Define las dependencias necesarias para el proyecto.
- *kubernetes.tf:* Define y gestiona la infraestructura de Kubernetes usando Terraform.

## Descripcion de la entrega
Patrones: 
- Saga
- Coreografía
- Orquestración

Se implementó una saga, que vive en un nuevo servicio llamado orquestración. Este servicio es distinto a los otros pues en el flujo que escogimos tenemos 2 agregaciones, autorización y anonimización, y consideramos que ninguna debe manejar el flujo de la transacción. Por lo tanto la saga implementa el módulo de orquestración de transacciones y las revierte. El módulo de orquestración escucha *Eventos de Integracion, los transforma en eventos de dominio y verifica qué comando debería ejecutar dado el evento. La ejecución de comandos se hace **siempre* desde el módulo de orquestración, pues es este el que maneja la lógica necesaria para saber qué comando tiene que ejecutar. 

Al entrar al detalle podemos ver lo siguiente:

1. Los módulos de ingestion y de seguridad tienen sólo un tópico de eventos
2. El módulo de autorización tiene dos tópicos de eventos
3. Los 3 servicios tienen 2 tópicos de comandos.
4. Los 3 servicios manejan la coreografía.
5. El módulo de orquestración sólo ejecuta los comandos necesarios al recibir un evento.

Se implementó una estrategía híbrida, similar aunque distinta a lo visto en el curso, donde el módulo de orquestración selecciona el comando correcto y los otros módulos le envían su "estado" a este módulo para determinar qué comando ejecutar. Cuando se revierten comandos por algún error se comunican los eventos al módulo de orquestración y este se encarga de ejecutar el comando necesario. En cada comando de reversión hay una coreografía con los otros servicios, es decir, cada servicio determina a quién tiene que enviar el evento de revertir. Esta solución es un poco no ortodoxa, pero nos parece que brinda flexibilidad en el código y, aunque mantiene un leve acomplamiento entre servicios esto sólo sucede cuando es necesario revertir trasacciones.

Otra parte interesante del trabajo fue la implementación de eventos gordos de integración que sirven para comunicar el estado al servicio de orquestración. Se decidió hacer esto para facilitar la reconstrucción del estado y poder ejecutar comandos válidos.

Por último, le módulo de orquestración tiene un Saga Log que se determina mediante la creación de filas en una tabla ordenada por el timestamp. Esto permite trackear y ver si las transacciones se ejecutaron de manera fácil. 

## Diagrama de Arquitecutra 
![image](https://github.com/user-attachments/assets/72a8fbdf-ef76-46c1-b1ca-be974142e92e)

### (*)Diagrama entrega 04
![image](https://github.com/user-attachments/assets/d4b8aa81-2218-4cef-ac91-c2c663447442)

## Experimentación POC
### Escenario de Calidad 1 (#1)

Hipotesis: Se van a poder procesar los mensajes aunque el servicio de ingestión de datos se caiga.

Experimento: Cambiar la cantídad máxima de pods por deployment a 0 para el servicio de ingestion.

Resultado: Se pudo comprobar que al utilizar tópicos con mensajes persistentes en Apache Pulsar los mensajes se envían hasta que sean "acknowledged", de lo contrario se vuelven a intentar procesar.

[Video](https://youtu.be/wX2igLdNuR4)

### Escenario de Calidad 2 (#3)

Hipotesis: Se van a poder procesar hasta 30,000 solicitudes en un día (~21 por minuto). Esto se puede lograr sin afectar los demás servicios pues se tienen tópicos de comandos, consultas y de eventos distintas que permiten el escalamiento. Si los tópicos de pulsar están llenos de mensajes de procesamiento entonces se puede verificar que los tópicos de lectura no se ven afectados.

Experimento: Llenar de validaciones de usuario, mientras se consulta la tabla de proyecciones de eventos de ingestion procesados.

Resultado: Aunque se pudo comprobar que se procesan todos los mensajes, la carga de 21 por mínuto es muy baja para tener un efecto en el sistema. El sistema procesa fácilmente 21 solicitudes por minúto.

[Video](https://youtu.be/7W3qY_n6Ijk)

### Escenario de Calidad 3 (#4)

Hipotesis: Al tener multiples instancias del servicio de autorización el sistema funciona sin problemas y puede soportar una tasa de menos de 0.5% de error cuando una de las instancias se cae.

Experimento: Habilitar 3 replicas del servicio de autorizacion, correr una prueba de carga con 10 solicitudes por segundo y tumbar una de las tres replicas. 

Resultado: Hubo un porcentaje de error mayor al esperado, pues las solicitudes que estaban en proceso no se pudieron enrutar a tiempo, aunque estemos usando el balanceador de carga de un servicio de kubernetes de load balancing. 

[Video](https://youtu.be/hY2yCLBa4Y0)


## Ejecutar Aplicación
- Para ejecutar el proyecto localmente , primero levante los contenedores de pulsar y de MySQL con el siguiente comando: 

docker compose up -d

- Cree el entorno virtual en python con los siguientes comandos: 

python3 -m venv venv
source venv/bin/activate

- Instale las dependencias de cada componente utilizando esl siguiente comando

pip install -r requirements.txt

- Ejecucion del Bff:

uvicorn bff.main:app --host localhost --port 8005 --reload

- Ejecucion del servicio de autorizacion:

flask --app autorizacion/api --debug run --port 5001

- Ejecucion del  servicio de ingestion:

uvicorn ingestion_datos.main:app --host localhost --port 8000 --reload

- Ejecucion del  servicio de orquestracion:

uvicorn ingestion_datos.main:app --host localhost --port 8000 --reload

- Ejecucion del servicio de seguridad:

flask --app seguridad/api --debug run --port 5002

## Request de ejemplo

### Happy Path

Para comprobar lo requerido para esta entrega puede ejecutar el siguiente request:

- *Endpoint:* /v1/sta/transaction
- *Método:* POST
- *Headers:* Content-Type='aplication/json'
- *Payload:* 

{
    "usuario": "dark-brandon",
    "imagen": "https://upload.wikimedia.org/wikipedia/commons/3/32/Dark_Brandon.jpg",
    "fecha_creacion": "2025-12-12"
}


### Error Paths

#### Error Validacion Usuario


- *Endpoint:* /v1/sta/transaction
- *Método:* POST
- *Headers:* Content-Type='aplication/json'
- *Payload:* 

{
    "usuario": "maligno",
    "imagen": "https://upload.wikimedia.org/wikipedia/commons/3/32/Dark_Brandon.jpg",
    "fecha_creacion": "2025-12-12"
}


#### Error Ingestion Imagen



{
    "usuario": "dark-brandon",
    "imagen": "maligno",
    "fecha_creacion": "2025-12-12"
}


### Dominios y SubDominios
- Ubicacion:  diagramas/DominiosSubdominios.cml
- Link: https://github.com/XCode-MISO/MISW4406-No-Monoliticas/blob/main/diagramas/DominiosSubdominios.cml

### Lenguaje Ubicuo
#### Convencion
![eventstorm-convencion](https://github.com/user-attachments/assets/00cf71cf-7570-45e9-9754-b62eeca2970d)

#### AS-IS
- Ubicacion:  diagramas/as-is/Event Storming - Lenguaje Ubicuo - AS IS.jpg
- Link: https://github.com/XCode-MISO/MISW4406-No-Monoliticas/blob/main/diagramas/as-is/Event%20Storming%20-%20Lenguaje%20Ubicuo%20-%20AS%20IS.jpg
- Diagrama: ![Event Storming - Lenguaje Ubicuo - AS IS](./diagramas/as-is/Event%20Storming%20-%20Lenguaje%20Ubicuo%20-%20AS%20IS.jpg)

#### TO-BE
- Ubicacion:  diagramas/to-be/ContextosAcotadosTOBE.png
- Link: https://github.com/XCode-MISO/MISW4406-No-Monoliticas/blob/main/diagramas/to-be/ContextosAcotadosTOBE.png
- Diagrama: ![image](https://github.com/user-attachments/assets/9cf15d82-a850-4909-9e0e-3d0f882afbe6)

### Mapas de Contexto
#### AS-IS
- Ubicacion:  diagramas/as-is/ContextosAcotados.cml
- Link: https://github.com/XCode-MISO/MISW4406-No-Monoliticas/blob/main/diagramas/as-is/ContextosAcotados.cml
- Diagrama : ![contexto-acotado](./diagramas/as-is/ContextosAcotados_ContextMap.png)

#### TO-BE
- Ubicacion:  diagramas/as-is/ContextosAcotados.cml
- Link: https://github.com/XCode-MISO/MISW4406-No-Monoliticas/blob/main/diagramas/to-be/ContextoAcotadoTOBE.cml
- Diagrama : ![contexto-acotado](./diagramas/to-be/ContextosAcotadosTOBE.png)
