# MoviData Panamá

## Optimización de consultas MongoDB — Fase 2

### 1. Objetivo

Evaluar y mejorar las consultas realizadas sobre la
colección movidata.viajes en MongoDB Atlas.

### 2. Volumen de datos

- Documentos: 1,000,000
- Tamaño lógico de datos: 406 MB
- Almacenamiento asignado: 105 MB
- Tamaño de índices: 47 MB
- Índices existentes: 2

### 3. Arquitectura implementada

Se utiliza el patrón Repository para separar el acceso
a MongoDB de la lógica de aplicación.

Componentes:

- domain/viaje.py
- repositories/i_readable_repository.py
- repositories/mongo_viajes_repository.py

### 4. Optimización mediante proyección

Se implementó buscar_con_proyeccion() para recuperar
únicamente los campos necesarios.

Prueba:

- Filtro: district = San Miguelito
- Campos: trip_id y district
- Registros solicitados: 5
- Resultado: prueba satisfactoria

### 5. Índices existentes

- _id_: índice predeterminado de MongoDB.
- trip_id_1: índice único para identificadores de viajes.

No existen índices específicos para district
ni transport_mode.

### 6. Rendimiento de conteos

Consulta por distrito:

- Documentos examinados: 1,000,000
- Claves examinadas: 0
- Tiempo: 744 ms

Consulta por transporte:

- Documentos examinados: 1,000,000
- Claves examinadas: 0
- Tiempo: 644 ms

### 7. Rendimiento de búsquedas limitadas

Consulta por trip_id:

- Documentos examinados: 1
- Claves examinadas: 1
- Tiempo reportado: 0 ms

Consulta por distrito:

- Documentos examinados: 21
- Claves examinadas: 0
- Tiempo reportado: 0 ms

Consulta por transporte:

- Documentos examinados: 8
- Claves examinadas: 0
- Tiempo reportado: 0 ms

Las búsquedas limitadas y los conteos completos
son operaciones diferentes y sus resultados no
constituyen una comparación directa.

### 8. Restricciones

El clúster gratuito de MongoDB Atlas se encuentra
cerca de su límite de almacenamiento.

No se crearon índices adicionales para evitar
incrementar el consumo sin evaluar previamente
su beneficio y costo.

### 9. Conclusiones

- El índice trip_id_1 permite búsquedas eficientes
  por identificador.
- Las proyecciones reducen los campos transferidos.
- Las consultas por distrito y transporte requieren
  evaluar índices para mejorar conteos completos.
- Se conservó el millón de registros originales.
- Las optimizaciones fueron verificadas mediante
  scripts de prueba.

### 10. Trabajo pendiente

- Evaluar alternativas para optimizar conteos.
- Estimar el costo de almacenamiento de nuevos índices.
- Ejecutar nuevas pruebas comparativas si se
  implementan optimizaciones adicionales.
- Solicitar revisión mediante Pull Request.
