# MoviData Panamá

## Documentación técnica — Arquitectura de Datos, Fase 2

### 1. Objetivo

Implementar una arquitectura de acceso a datos mediante
el patrón Repository, utilizando Python y MongoDB Atlas
para consultar y analizar viajes de movilidad urbana.

### 2. Base de datos

- Motor: MongoDB Atlas
- Base de datos: movidata
- Colección: viajes
- Documentos cargados: 1,000,000
- Fuente: dataset de viajes MoviData

### 3. Arquitectura implementada

Componentes principales:

- domain/viaje.py
- repositories/i_readable_repository.py
- repositories/mongo_viajes_repository.py

El modelo Viaje representa los datos del dominio.

IReadableRepository define la interfaz de lectura.

MongoViajesRepository implementa las consultas
contra MongoDB Atlas.

### 4. Consultas implementadas

Se implementaron consultas para:

- Buscar viajes por distrito.
- Consultar viajes por ruta.
- Contar viajes por tipo de transporte.
- Agrupar viajes por distrito.
- Agrupar viajes por hora.

Las agregaciones utilizan operadores MongoDB
como $group, $sum, $sort y $limit.

### 5. Validación de calidad

Resultados sobre 1,000,000 de documentos:

- Campos obligatorios faltantes o vacíos: 0.
- Tipos diferentes de string en seis campos: 0.
- Horas con formato inválido: 0.
- Fechas con formato inválido: 0.
- Índice único de trip_id: confirmado.

La validación de fechas comprueba el formato,
no todas las reglas del calendario.

### 6. Índices existentes

Índices identificados:

- _id_
- trip_id_1 (único)

No se encontraron índices específicos para
district ni transport_mode.

### 7. Rendimiento

Consulta por trip_id:

- Documentos examinados: 1.
- Índice utilizado: trip_id_1.

Conteo por distrito San Miguelito:

- Documentos examinados: 1,000,000.
- Tiempo registrado: 739 ms.
- Claves de índice examinadas: 0.

Conteo por transporte Metrobus:

- Documentos examinados: 1,000,000.
- Tiempo registrado: 646 ms.
- Claves de índice examinadas: 0.

Los tiempos corresponden a una medición
y pueden variar entre ejecuciones.

### 8. Almacenamiento

Estadísticas obtenidas mediante dbStats:

- Tamaño lógico de datos: 406 MB.
- Almacenamiento reportado: 105 MB.
- Tamaño de índices: 47 MB.

Estas estadísticas no equivalen directamente
al consumo total mostrado en Atlas.

### 9. Decisiones de arquitectura

- Se utiliza el patrón Repository para separar
  la lógica de acceso a datos del dominio.
- Se emplea un índice único sobre trip_id.
- Las consultas analíticas se ejecutan en Atlas.
- No se crean índices adicionales sin evaluar
  previamente el almacenamiento disponible.
- Los archivos .env y los datasets grandes
  no deben publicarse en GitHub.

### 10. Recomendaciones

- Evaluar índices para district y transport_mode
  cuando exista capacidad de almacenamiento.
- Medir el rendimiento con diferentes consultas.
- Validar las fechas como valores de calendario.
- Considerar tipos nativos para fechas y horas
  en futuras versiones del modelo.
- Mantener pruebas automatizadas del Repository.

### 11. Conclusión

Se implementó y probó una arquitectura de lectura
para MoviData Panamá sobre MongoDB Atlas.

Las consultas y agregaciones funcionan sobre
1,000,000 de documentos.

Se identificaron oportunidades de optimización
sin modificar los datos existentes.
