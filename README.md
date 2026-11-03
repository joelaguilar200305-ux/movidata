# MoviData Panamá

Análisis de Big Data de movilidad urbana en el transporte público de Panamá (Metro y Metrobus). Proyecto de Programación 2 (EID 1012), ITSE.

## Requisitos

- Python 3.12 o superior
- MongoDB 7.x corriendo en local (localhost:27017)
- Git y VS Code

## Instalación

Clonar el repositorio y entrar a la carpeta:

    git clone https://github.com/joelaguilar200305-ux/movidata.git
    cd movidata

Crear las carpetas que Git ignora:

    mkdir data, exports

Crear y activar el entorno virtual (Windows PowerShell):

    python -m venv .venv
    .venv\Scripts\Activate.ps1

Instalar las dependencias:

    pip install -r requirements.txt

## Ejecución

Generar el dataset, ejecutando el script desde la carpeta data:

    cd data
    python ..\scripts\generar_dataset_movidata.py
    cd ..

Se crea data\viajes_movidata.csv con 2 000 000 de viajes. La semilla fija (SEED = 2025) hace que todos obtengan los mismos datos. El archivo no se sube a GitHub.

Cargar los datos a MongoDB: se completa cuando esté listo el DataLoader.

## Integrantes y roles

| Integrante            | Rol                       |
| --------------------- | ------------------------- |
| Yoel Aguilar          | Líder técnico             |
| (Rodrigo Sanchez)     | Arquitecto de datos       |
| (Pedro Garcia)        | Desarrollador de ingesta  |
| (Angel Cardenas)      | Desarrollador de análisis |
| (Fernando Santamaria) | Documentación y BI        |

## Avance de arquitectura de datos - MongoDB Atlas

Se configuro la conexion de Python con MongoDB Atlas
para realizar la carga progresiva de viajes.

### Resultados obtenidos

- Base de datos: movidata
- Coleccion: viajes
- Registros cargados y verificados: 30000
- Carga automatizada en bloques de 1000 registros
- Control de duplicados mediante trip_id
- Conexion exitosa con MongoDB Atlas

### Ejecucion de la carga

Desde la terminal de VS Code:

    python carga_mongo.py --inicio 0
    python carga_mongo.py --inicio 1000
    python carga_mongo.py --inicio 2000
    python carga_mongo.py --inicio 3000
    python carga_mongo.py --inicio 4000
    python carga_mongo.py --inicio 5000
    python carga_mongo.py --inicio 6000
    python carga_mongo.py --inicio 7000
    python carga_mongo.py --inicio 8000
    python carga_mongo.py --inicio 9000

### Proxima etapa

Automatizar la carga progresiva de registros
y supervisar el almacenamiento de MongoDB Atlas.
