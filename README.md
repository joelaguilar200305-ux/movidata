# MoviData Panamá

## Descripción del proyecto

MoviData Panamá es un proyecto universitario de Big Data orientado al análisis de movilidad urbana en el transporte público de Panamá, específicamente Metro y Metrobus.

**Institución:** ITSE
**Asignatura:** Programación 2 (EID 1012)

## Objetivo general

Desarrollar una solución de análisis de datos para estudiar los patrones de movilidad urbana del transporte público de Panamá utilizando Python y MongoDB.

## Tecnologías utilizadas

- Python 3.12 o superior
- MongoDB Atlas
- MongoDB 7.x
- PyMongo
- Pandas
- NumPy
- python-dotenv
- Git y GitHub
- Visual Studio Code

## Requisitos

- Python 3.12 o superior
- Acceso a MongoDB Atlas
- Git
- Visual Studio Code
- Conexión a Internet

## Instalación

### Clonar el repositorio

    git clone https://github.com/joelaguilar200305-ux/movidata.git
    cd movidata

### Crear el entorno virtual

    python -m venv .venv

### Activar el entorno virtual

    .\.venv\Scripts\Activate.ps1

### Instalar dependencias

    pip install -r requirements.txt

## Configuración de MongoDB Atlas

Crear un archivo .env en la raíz del proyecto con la variable MONGODB_URI.

    MONGODB_URI=mongodb+srv://USUARIO:CONTRASENA@CLUSTER/

El archivo .env contiene credenciales privadas y no debe subirse a GitHub.

## Generación del dataset

El proyecto contempla un dataset sintético de 2,000,000 de registros de viajes del transporte público de Panamá.

El archivo CSV se almacena en:

    data/viajes_movidata.csv

Este archivo no se sube a GitHub debido a su tamaño.

## Arquitectura de datos

El procesamiento sigue las siguientes etapas:

1. Generación del dataset.
2. Lectura de archivos CSV.
3. Procesamiento de registros mediante Python.
4. Conexión con MongoDB Atlas.
5. Inserción progresiva por bloques.
6. Control de duplicados mediante trip_id.
7. Verificación de documentos almacenados.
8. Preparación para análisis de movilidad.

## Base de datos

- Base de datos: movidata
- Colección: viajes
- Identificador único: trip_id
- Motor de almacenamiento: MongoDB Atlas

## Carga progresiva de datos

La carga se realiza utilizando el archivo carga_mongo.py.

### Parámetros

- --inicio: posición inicial del CSV.
- --cantidad: cantidad de registros a procesar.

### Ejemplo de ejecución

    python carga_mongo.py --inicio 100000 --cantidad 10000

### Configuración de carga

- Bloques internos: 1000 registros.
- Máximo por ejecución: 10000 registros.
- Control de duplicados mediante trip_id.
- Inserción mediante operaciones bulk_write.

## Resultados obtenidos

### Avance de carga

- Base de datos: movidata
- Colección: viajes
- Registros cargados y verificados: 1000000
- Bloques internos: 1000 registros
- Máximo por ejecución: 10000 registros
- Control de duplicados mediante trip_id
- Conexión exitosa con MongoDB Atlas

### Estado de la carga

Se completó la carga progresiva de 200000 documentos de viajes del transporte público de Panamá.

La carga se realizó utilizando Python, PyMongo y MongoDB Atlas.

## Control de almacenamiento

El proyecto utiliza un clúster gratuito de MongoDB Atlas.

La capacidad indicada para el clúster es de 512 MB.

Se supervisa el almacenamiento para evitar superar los límites del servicio.

## Próxima etapa

- Continuar la carga progresiva de documentos.
- Supervisar el almacenamiento de MongoDB Atlas.
- Mejorar el control de errores.
- Preparar consultas de análisis de movilidad.
- Analizar rutas, horarios y demanda de transporte.
- Documentar los resultados obtenidos.

## Control de versiones

El proyecto utiliza Git y GitHub para registrar los avances.

### Rama de trabajo

    feature/movidata-conexion-atlas

Cada avance debe registrarse mediante commits.

Los archivos .env y CSV grandes no deben subirse a GitHub.

## Integrantes y roles

| Integrante          | Rol                       |
| ------------------- | ------------------------- |
| Yoel Aguilar        | Líder técnico             |
| Rodrigo Sanchez     | Arquitecto de datos       |
| Pedro Garcia        | Desarrollador de ingesta  |
| Angel Cardenas      | Desarrollador de análisis |
| Fernando Santamaria | Documentación y BI        |

## Estado del proyecto

La conexión entre Python y MongoDB Atlas está funcionando.

Se ha implementado la carga progresiva de documentos mediante Python.

El proyecto continúa en desarrollo para ampliar el almacenamiento y realizar análisis de movilidad urbana en Panamá.
