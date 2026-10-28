# Diccionario de datos: MoviData Panamá

Describe los 16 campos del archivo `viajes_movidata.csv` (2,000,000 de viajes y 120,000 tarjetas, de junio a noviembre de 2024). Coincide con el [diagrama de clases](class-diagram.png): la última columna indica en qué clase vive cada campo.

## Campos

| Campo | Tipo en Python | Tipo en MongoDB | Oblig. | Descripción | Regla / validación | Ejemplo | Clase |
|---|---|---|---|---|---|---|---|
| `trip_id` | `str` | string | Sí | Identificador único del viaje. | Único. `VJE` + 9 dígitos. | `VJE000000001` | `Viaje` |
| `card_id` | `str` | string | Sí | Identificador de la tarjeta (usuario). | `TRJ` + 7 dígitos. Enlaza el viaje con su tarjeta. | `TRJ0014553` | `Tarjeta` y `Viaje` |
| `user_type` | `str` | string | Sí | Tipo de usuario. | Uno de: `Regular`, `Estudiante`, `Jubilado`, `Turista`. | `Estudiante` | `Tarjeta` |
| `district` | `str` | string | Sí | Distrito de residencia del usuario. | Uno de: `Panama`, `San Miguelito`, `Arraijan`, `La Chorrera`, `Colon`. | `San Miguelito` | `Tarjeta` |
| `transport_mode` | `str` | string | Sí | Modo de transporte. | `Metro` o `Metrobus`. | `Metrobus` | `Viaje` |
| `route_line` | `str` | string | Sí | Línea del Metro o ruta troncal del Metrobus. | Metro: `Linea 1` o `Linea 2`. Metrobus: una de las 10 rutas troncales (por ejemplo `C800-Albrook`). | `M500-Las Cumbres` | `Viaje` |
| `origin` | `str` | string | Sí | Estación o parada de origen. | Una de las 17 estaciones del catálogo. Distinta del destino. | `Aeropuerto` | `Viaje` |
| `destination` | `str` | string | Sí | Estación o parada de destino. | Una de las 17 estaciones del catálogo. Distinta del origen. | `Villa Lucre` | `Viaje` |
| `boarding_datetime` | `datetime` | date | Sí | Fecha y hora de abordaje. | Fecha válida. Se guarda como fecha, no como texto. Datos entre 2024-06-01 y 2024-11-30. | `2024-08-19 13:37:00` | `Viaje` |
| `day_of_week` | `str` | string | Sí | Día de la semana del viaje. | Nombre en inglés: `Monday` a `Sunday`. | `Monday` | `Viaje` |
| `hour` | `int` | int | Sí | Hora de abordaje. | Entero de 0 a 23. | `13` | `Viaje` |
| `distance_km` | `float` | double | Sí | Distancia aproximada del viaje, en kilómetros. | Mayor o igual a 0. | `15.76` | `Viaje` |
| `duration_min` | `float` | double | Sí | Duración aproximada del viaje, en minutos. | Mayor o igual a 0. | `50.1` | `Viaje` |
| `fare` | `float` | double | Sí | Tarifa pagada, en balboas (PAB). | Mayor o igual a 0. Con descuento de 50 % para `Estudiante` y `Jubilado`. | `0.12` | `Viaje` |
| `payment_method` | `str` | string | Sí | Medio de pago. | Uno de: `Tarjeta_Metro`, `Tarjeta_bancaria_NFC`, `QR_movil`. | `Tarjeta_Metro` | `Viaje` |
| `weather` | `str` | string | Sí | Clima estimado durante el viaje. | Uno de: `Soleado`, `Nublado`, `Lluvia`, `Tormenta`. | `Lluvia` | `Viaje` |

## Modelo en MongoDB

- **Base de datos:** `movidata`. **Colección:** `trips`.
- Cada documento representa **un viaje**, con los campos de la tabla anterior.
- **Índices recomendados:** `card_id`, `boarding_datetime`, `route_line` y `transport_mode`.
- **Carga por lotes** (inserción masiva), porque son 2,000,000 de registros.

## Valores de control del dataset

Con la semilla fija `SEED = 2025`, cualquier computadora genera los mismos datos:

| Dato | Valor |
|---|---|
| Registros | 2,000,000 |
| Tarjetas únicas | 120,000 |
| Recaudación total simulada | 504,910.51 PAB |
| Duración promedio | 23.7 min |
| Metrobus / Metro | 1,100,281 / 899,719 |
