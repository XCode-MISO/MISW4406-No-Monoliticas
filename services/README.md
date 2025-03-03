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

 ```bash
venv\Scripts\activate
 ```
    
 - Instalar dependencia: 

 ```bash
    pip install -r requirements.txt
    pip install -r ingestion_datos-requirements.txt
 ```

 - Para ejecutar el docker-compose hacer lo siguiente

 ```bash
docker build . -f seguridad.Dockerfile -t seguridad/flask
docker compose up -d
 ```

 - Ejecutar Servidor Seguridad Http en modo debug:

 ```bash
    flask --app seguridad/api --debug run
 ```

- Ejecutar Servidor ingestion-datos en modo debug:

```bash
uvicorn ingestion_datos.main:app --host localhost --port 8000 --reload
```

## Desplegar aplicación

### Aplicación en Google Cloud

Requerimientos:
1. Terraform
2. Helm
3. Configuración de Google Cloud
4. Configuración de Kubernetes para el cluster de google cloud donde se desplegará

Pasos:

```bash
# en la carpeta de services ~ ./services
terraform init
terraform plan
terraform apply
```

Para destruir se usa

```bash
terraform destroy
```

### Pulsar en Google Cloud

#### Desplegar pulsar en un cluster de kubernetes de GKE

```bash
# Tomado de: https://pulsar.apache.org/docs/2.10.x/helm-prepare/
PROJECT=nomonoliticas-452502 REGION=us-central1 ZONE_EXTENSION=a sh ./pulsar/scripts/pulsar/gke_bootstrap_script.sh up
```

```bash
helm repo add apache https://pulsar.apache.org/charts
helm repo update
helm install pulsar apache/pulsar \
    --timeout 10m \
    --set initialize=true
```

#### Tumbar pulsar de GKE

```bash
# Tomado de: https://pulsar.apache.org/docs/2.10.x/helm-prepare/
sh ./pulsar/scripts/pulsar/gke_bootstrap_script.sh down
```