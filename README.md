# MoviData Panamá

## Descripción del proyecto

MoviData Panamá es un proyecto universitario de Big Data orientado al análisis de movilidad urbana en el transporte público de Panamá, específicamente Metro y Metrobus.

**Institución:** ITSE

**Asignatura:** Programación 2 (EID 1012)

## Objetivo general

Desarrollar una solución de análisis de datos para estudiar los patrones de movilidad urbana del transporte público de Panamá utilizando Python, MongoDB Atlas y patrones de diseño de software.

## Tecnologías utilizadas

- Python 3.12 o superior
- MongoDB Atlas
- PyMongo
- Pandas
- NumPy
- python-dotenv
- Git y GitHub
- Visual Studio Code

## Requisitos

- Python 3.12 o superior
- Acceso autorizado a MongoDB Atlas
- Git
- Visual Studio Code
- Conexión a Internet
- Dependencias incluidas en requirements.txt

## Instalación

### Clonar el repositorio

```powershell
git clone https://github.com/joelaguilar200305-ux/movidata.git
cd movidata
```

### Crear el entorno virtual

```powershell
python -m venv .venv
```

### Activar el entorno virtual

En Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

## Configuración de MongoDB Atlas

La conexión a MongoDB se administra mediante el archivo:

`config/conexion_mongo.py`

Este componente implementa una conexión centralizada mediante el patrón Singleton.

### Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```dotenv
MONGODB_URI=TU_URI_PRIVADA_DE_MONGODB_ATLAS
MONGODB_DATABASE=movidata
MONGODB_COLLECTION=viajes
```

La URI debe reemplazarse por la conexión real proporcionada por MongoDB Atlas.

**Importante:**

- El archivo `.env` contiene credenciales privadas.
- No debe subirse a GitHub.
- La configuración permite cambiar la base de datos y la colección sin modificar el código del Repository.
- La colección `viajes` corresponde a los datos actualmente cargados y al diagrama de flujo del proyecto.

## Generación del dataset

El proyecto contempla un dataset sintético de 2,000,000 de registros de viajes del transporte público de Panamá.

El archivo generado se almacena en:

`data/viajes_movidata.csv`

El CSV contiene información sobre:

- Identificadores de viajes.
- Tipo de transporte.
- Distrito.
- Ruta.
- Fecha y hora.
- Otros atributos de movilidad.

El archivo CSV no debe publicarse en GitHub debido a su tamaño.

## Arquitectura del proyecto

La arquitectura utiliza separación por capas y patrones de diseño para organizar las responsabilidades del sistema.

### Estructura de carpetas

```text
movidata/
|
|-- config/
|   |-- __init__.py
|   |-- conexion_mongo.py
|
|-- domain/
|   |-- __init__.py
|   |-- viaje.py
|
|-- repositories/
|   |-- __init__.py
|   |-- i_viaje_repository.py
|   |-- mongo_viaje_repository.py
|
|-- analysis/
|-- services/
|-- utils/
|-- scripts/
|-- tests/
|-- docs/
|-- data/
|-- exports/
|
|-- carga_mongo.py
|-- .env
|-- .gitignore
|-- requirements.txt
|-- README.md
```

Los demás componentes de análisis, servicios e ingesta se desarrollan de acuerdo con las responsabilidades asignadas a cada integrante del equipo.

### Patrón Repository

El acceso a los datos se organiza mediante una interfaz y una implementación concreta.

**Interfaz:**

`repositories/i_viaje_repository.py`

Clase:

`IViajeRepository`

**Implementación MongoDB:**

`repositories/mongo_viaje_repository.py`

Clase:

`MongoViajeRepository`

El patrón Repository permite separar la lógica de acceso a datos del resto de la aplicación.

### Métodos del Repository

Se implementaron los siguientes métodos:

- `buscar_por_id()`
- `buscar_por_filtro()`
- `contar_documentos()`
- `agregar()`
- `buscar_con_proyeccion()`

También se dispone del método `cerrar()` para administrar el cierre de la conexión.

### Conexión centralizada

La clase `MongoConnection`, ubicada en `config/conexion_mongo.py`, administra la conexión con MongoDB Atlas y obtiene los parámetros desde el archivo `.env`.

El objetivo es evitar que los repositorios mantengan nombres fijos de base de datos, colección o credenciales.

## Flujo de procesamiento de datos

El proyecto contempla las siguientes etapas:

1. Generación del dataset sintético.
2. Lectura de registros CSV.
3. Procesamiento y validación mediante Python.
4. Conexión a MongoDB Atlas.
5. Inserción progresiva por bloques.
6. Control de duplicados mediante `trip_id`.
7. Verificación de documentos almacenados.
8. Consultas mediante el patrón Repository.
9. Análisis de movilidad urbana.
10. Preparación de resultados para visualización.

## Base de datos

**Motor:** MongoDB Atlas

**Base de datos:** movidata

**Colección:** viajes

**Identificador de viaje:** trip_id

**Documentos cargados y verificados:** 1,000,000

### Índices existentes

Se identificaron dos índices:

- `_id_`: índice predeterminado de MongoDB.
- `trip_id_1`: índice único para identificar los viajes.

No se crearon índices adicionales para distrito o transporte debido a las limitaciones de almacenamiento del clúster gratuito.

## Carga progresiva de datos

La carga de registros se realizó utilizando el archivo:

`carga_mongo.py`

### Parámetros

- `--inicio`: posición inicial del CSV.
- `--cantidad`: cantidad de registros a procesar.

### Ejemplo de ejecución

```powershell
python carga_mongo.py --inicio 100000 --cantidad 10000
```

### Configuración de carga

- Bloques internos de 1,000 registros.
- Máximo de 10,000 registros por ejecución.
- Control de duplicados mediante `trip_id`.
- Operaciones de escritura utilizando `bulk_write`.
- Inserción progresiva con seguimiento de resultados.

### Resultado final de la carga

Se completó y verificó la carga de:

**1,000,000 de documentos en MongoDB Atlas.**

Las cargas anteriores de 200,000, 250,000 y 500,000 documentos corresponden a etapas del proceso.

La carga acumulada verificada alcanzó 1,000,000 de documentos.

Actualmente no se realizarán nuevas cargas masivas debido al almacenamiento disponible en el clúster gratuito.

## Consultas y agregaciones

Se implementaron consultas sobre datos reales de movilidad urbana.

### Consultas disponibles

- Búsqueda de viajes por identificador.
- Búsqueda de viajes por distrito.
- Búsqueda de viajes por tipo de transporte.
- Búsqueda de viajes por ruta.
- Conteo de documentos.
- Agrupación de viajes por distrito.
- Agrupación de viajes por hora.
- Recuperación selectiva de campos.

### Operadores MongoDB utilizados

- `$match`
- `$group`
- `$sum`
- `$sort`
- `$limit`
- `$toInt`

La conversión `$toInt` se utiliza para ordenar correctamente las horas almacenadas como texto.

## Resultados del análisis

### Distribución por tipo de transporte

Resultados obtenidos sobre 1,000,000 de documentos:

| Transporte | Total de viajes |
| ---------- | --------------: |
| Metrobus   |         550,533 |
| Metro      |         449,467 |
| Total      |       1,000,000 |

### Distritos con mayor cantidad de viajes

| Distrito      |   Total |
| ------------- | ------: |
| Panamá        | 460,154 |
| San Miguelito | 219,913 |
| Arraiján      | 138,092 |
| La Chorrera   | 131,826 |
| Colón         |  50,015 |

Estas cifras corresponden a los resultados obtenidos mediante agregaciones ejecutadas en MongoDB Atlas.

## Validación de calidad de datos

Se desarrollaron pruebas para evaluar la estructura y consistencia de los documentos almacenados.

### Resultados

- Documentos evaluados: 1,000,000.
- Campos obligatorios faltantes o vacíos: 0.
- Tipos de datos incorrectos en los seis campos evaluados: 0.
- Horas con formato inválido: 0.
- Fechas con formato inválido: 0.
- Índice único sobre `trip_id`: confirmado.

La validación de fechas comprueba su formato textual, pero no garantiza por sí sola la validez de todas las fechas del calendario.

## Optimización de consultas

Se incorporó el método:

`buscar_con_proyeccion()`

Este método permite recuperar únicamente los campos necesarios de cada documento.

### Ejemplo de uso

```python
viajes = repositorio.buscar_con_proyeccion(
    {"district": "San Miguelito"},
    ["trip_id", "district"],
    limite=5
)
```

La proyección reduce la información transferida y procesada por Python, sin modificar los documentos almacenados.

No sustituye el uso de índices para consultas que necesitan examinar grandes cantidades de registros.

## Evaluación de rendimiento

Se realizaron pruebas utilizando `explain()`.

### Búsquedas limitadas

| Consulta       | Documentos examinados | Claves examinadas |
| -------------- | --------------------: | ----------------: |
| Por trip_id    |                     1 |                 1 |
| Por distrito   |                    21 |                 0 |
| Por transporte |                     8 |                 0 |

### Consultas de conteo completo

| Consulta      | Documentos examinados | Tiempo registrado |
| ------------- | --------------------: | ----------------: |
| San Miguelito |             1,000,000 |            744 ms |
| Metrobus      |             1,000,000 |            644 ms |

Los tiempos corresponden a una ejecución y pueden variar.

Los resultados demuestran que las búsquedas limitadas y los conteos completos tienen costos diferentes.

## Control de almacenamiento

El proyecto utiliza un clúster gratuito de MongoDB Atlas.

**Capacidad observada:** 512 MB.

En una de las verificaciones realizadas:

- Consumo mostrado por Atlas: 454.23 MB.
- Porcentaje utilizado: aproximadamente 89 %.
- Espacio restante aproximado: 57.77 MB.

Estos valores corresponden a una medición del clúster y pueden cambiar.

### Decisiones técnicas

- Mantener los 1,000,000 de registros existentes.
- Evitar nuevas cargas masivas.
- No duplicar colecciones.
- No crear índices adicionales sin evaluar su costo.
- Priorizar consultas limitadas y proyecciones.
- Supervisar el almacenamiento disponible.

## Pruebas del proyecto

Las pruebas del Repository y de las consultas se encuentran en la carpeta `tests/`.

### Prueba del Repository

```powershell
python -m tests.probar_repository
```

### Prueba de consultas avanzadas

```powershell
python -m tests.probar_consultas_avanzadas
```

### Prueba de proyección

```powershell
python -m tests.probar_proyeccion
```

### Validación de documentos

```powershell
python -m tests.validar_documentos
```

### Validación de calidad

```powershell
python -m tests.validar_calidad_datos
```

### Análisis de rendimiento

```powershell
python -m tests.analizar_rendimiento
```

### Comparación de índices

```powershell
python -m tests.comparar_rendimiento_indices
```

Estas pruebas deben ejecutarse desde la raíz del proyecto, con el entorno virtual activo y la conexión a MongoDB Atlas correctamente configurada.

Después de cualquier modificación de arquitectura deben ejecutarse nuevamente para comprobar la compatibilidad de los componentes.

## Documentación técnica

Los principales documentos de arquitectura y optimización son:

- `docs/arquitectura_datos_fase2.md`
- `docs/optimizacion_consultas_fase2.md`

Estos archivos documentan el patrón Repository, las consultas, las validaciones y las decisiones técnicas.

## Control de versiones

El proyecto utiliza Git y GitHub.

### Repositorio

https://github.com/joelaguilar200305-ux/movidata

### Ramas

- `main`: rama principal.
- `develop`: rama de integración del equipo.
- `feature/movidata-conexion-atlas`: rama utilizada para implementar la conexión y la carga inicial.
- `feature/movidata-optimizacion-consultas`: rama de optimización y correcciones del Repository.

### Integraciones

El Pull Request #5 fue aprobado e integrado a `develop`.

El Pull Request #6 contiene las optimizaciones y las correcciones pendientes de revisión e integración.

### Buenas prácticas

- Crear commits por cada avance.
- Trabajar en ramas independientes.
- Solicitar revisión mediante Pull Requests.
- No modificar directamente `develop` sin coordinación.
- No publicar contraseñas ni credenciales.
- Mantener `.env` y datasets grandes fuera de GitHub.

## Integrantes y roles

| Integrante          | Rol                       |
| ------------------- | ------------------------- |
| Yoel Aguilar        | Líder técnico             |
| Rodrigo Sanchez     | Arquitecto de datos       |
| Pedro Garcia        | Desarrollador de ingesta  |
| Angel Cardenas      | Desarrollador de análisis |
| Fernando Santamaria | Documentación y BI        |

## Estado actual del proyecto

Se completó la carga y verificación de 1,000,000 de documentos en MongoDB Atlas.

Se desarrollaron y probaron el patrón Repository, las consultas con filtros, las agregaciones, la validación de datos y el análisis de rendimiento.

También se implementaron consultas con proyección de campos y se inició la adecuación de la arquitectura a la estructura de carpetas definida por el profesor.

Las correcciones de arquitectura deben validarse nuevamente antes de integrarse a `develop`.

## Actividades pendientes

- Finalizar las correcciones solicitadas por el líder técnico.
- Comprobar la conexión centralizada desde el Repository.
- Ejecutar nuevamente las pruebas después de los cambios.
- Actualizar las referencias de clases y módulos.
- Revisar que no existan archivos antiguos innecesarios.
- Verificar la protección de credenciales.
- Publicar los commits de corrección.
- Obtener la aprobación del Pull Request #6.
- Integrar los cambios autorizados a `develop`.

## Conclusión

MoviData Panamá dispone de una base de datos de movilidad urbana con 1,000,000 de documentos cargados y verificados en MongoDB Atlas.

Se implementaron componentes para el acceso estructurado a datos, consultas avanzadas, validación de calidad y evaluación del rendimiento.

El proyecto continúa su desarrollo siguiendo la arquitectura establecida por el profesor y las responsabilidades asignadas a cada integrante.
