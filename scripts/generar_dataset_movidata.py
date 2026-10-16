"""
generar_dataset_movidata.py
Generador de dataset ficticio para el proyecto MoviData Panama.
Genera viajes sinteticos de transporte publico (Metro / Metrobus)
para analisis de Big Data de movilidad urbana.

Uso:
    python generar_dataset_movidata.py

Salida:
    viajes_movidata.csv  (2,000,000 de registros por defecto)

Requisitos:
    pip install numpy pandas
"""

import numpy as np
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuracion general
# ---------------------------------------------------------------------------
NUM_RECORDS = 2_000_000        # cantidad de viajes a generar
NUM_CARDS = 120_000            # cantidad de tarjetas (usuarios) unicas
SEED = 2025                    # semilla para reproducibilidad
OUTPUT_FILE = "viajes_movidata.csv"

rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------------------
# Catalogos base
# ---------------------------------------------------------------------------
user_types = np.array(["Regular", "Estudiante", "Jubilado", "Turista"])
user_weights = np.array([0.68, 0.20, 0.09, 0.03])

transport_modes = np.array(["Metro", "Metrobus"])
mode_weights = np.array([0.45, 0.55])

payment_methods = np.array(["Tarjeta_Metro", "Tarjeta_bancaria_NFC", "QR_movil"])
payment_weights = np.array([0.78, 0.14, 0.08])

# Estaciones de la Linea 1 y Linea 2 del Metro (nombres reales de referencia)
metro_stations = np.array([
    "Albrook", "San Miguelito", "Los Andes", "Rana de Oro", "El Ingenio",
    "Via Argentina", "Iglesia del Carmen", "5 de Mayo", "12 de Octubre",
    "Fernandez de Cordoba", "San Isidro", "Pedregal", "Villa Lucre",
    "Brisas del Golf", "Cincuentenario", "Corredor Sur", "Aeropuerto",
])

# Rutas troncales de Metrobus (referenciales)
metrobus_routes = np.array([
    "C800-Albrook", "C820-Tocumen", "M400-San Miguelito", "M600-Chorrera",
    "C120-Costa del Este", "C640-24 de Diciembre", "M300-Los Andes",
    "C210-Cinta Costera", "M500-Las Cumbres", "C900-Panama Viejo",
])

districts = np.array([
    "Panama", "San Miguelito", "Arraijan", "La Chorrera", "Colon",
])
district_weights = np.array([0.46, 0.22, 0.14, 0.13, 0.05])

weather = np.array(["Soleado", "Nublado", "Lluvia", "Tormenta"])
weather_weights = np.array([0.50, 0.28, 0.18, 0.04])

# ---------------------------------------------------------------------------
# Generacion de tarjetas (dimension usuario)
# ---------------------------------------------------------------------------
print(f"Generando {NUM_CARDS:,} tarjetas...")
card_ids = np.array([f"TRJ{n:07d}" for n in range(1, NUM_CARDS + 1)])
card_user_type = rng.choice(user_types, NUM_CARDS, p=user_weights)
card_district = rng.choice(districts, NUM_CARDS, p=district_weights)

# ---------------------------------------------------------------------------
# Generacion de viajes (hechos) - vectorizado
# ---------------------------------------------------------------------------
print(f"Generando {NUM_RECORDS:,} viajes...")
idx = rng.integers(0, NUM_CARDS, NUM_RECORDS)

# Fecha base: 6 meses de operacion
start = datetime(2024, 6, 1)
rand_seconds = rng.integers(0, 183 * 24 * 3600, NUM_RECORDS)
ts = pd.to_datetime(start) + pd.to_timedelta(rand_seconds, unit="s")

# Sesgo horario hacia horas pico (7-9am y 5-7pm)
peak = rng.random(NUM_RECORDS)
hour = np.where(
    peak < 0.30, rng.integers(7, 9, NUM_RECORDS),           # pico manana
    np.where(peak < 0.60, rng.integers(17, 19, NUM_RECORDS),  # pico tarde
             rng.integers(5, 23, NUM_RECORDS)),                # resto del dia
)
minute = rng.integers(0, 60, NUM_RECORDS)
# Reemplazamos la hora del timestamp por la hora con sesgo pico
ts = ts.normalize() + pd.to_timedelta(hour, unit="h") + pd.to_timedelta(minute, unit="m")

mode = rng.choice(transport_modes, NUM_RECORDS, p=mode_weights)

# Linea del Metro o ruta troncal del Metrobus segun el modo
metro_lines = np.array(["Linea 1", "Linea 2"])
line_idx = rng.integers(0, len(metro_lines), NUM_RECORDS)
route_idx = rng.integers(0, len(metrobus_routes), NUM_RECORDS)
route_line = np.where(mode == "Metro", metro_lines[line_idx],
                      metrobus_routes[route_idx])

# Origen y destino: siempre paradas distintas del catalogo compartido
station_idx = rng.integers(0, len(metro_stations), NUM_RECORDS)
dest_station_idx = (station_idx + rng.integers(1, len(metro_stations),
                    NUM_RECORDS)) % len(metro_stations)
origin = metro_stations[station_idx]
destination = metro_stations[dest_station_idx]

# Distancia y duracion correlacionadas
distance_km = np.round(rng.gamma(shape=2.2, scale=3.0, size=NUM_RECORDS) + 0.5, 2)
distance_km = np.clip(distance_km, 0.5, 45.0)
# Velocidad media ~18 km/h + ruido -> duracion en minutos
duration_min = np.round(distance_km / 18.0 * 60 +
                        rng.normal(0, 4, NUM_RECORDS), 1)
duration_min = np.clip(duration_min, 2.0, 120.0)

# Tarifa: Metro base 0.35, Metrobus 0.25; descuentos por tipo de usuario
base_fare = np.where(mode == "Metro", 0.35, 0.25)
user_type_row = card_user_type[idx]
discount = np.where(np.isin(user_type_row, ["Estudiante", "Jubilado"]), 0.5, 1.0)
fare = np.round(base_fare * discount, 2)

payment = rng.choice(payment_methods, NUM_RECORDS, p=payment_weights)
weather_row = rng.choice(weather, NUM_RECORDS, p=weather_weights)

print("Ensamblando DataFrame...")
df = pd.DataFrame({
    "trip_id": [f"VJE{n:09d}" for n in range(1, NUM_RECORDS + 1)],
    "card_id": card_ids[idx],
    "user_type": user_type_row,
    "district": card_district[idx],
    "transport_mode": mode,
    "route_line": route_line,
    "origin": origin,
    "destination": destination,
    "boarding_datetime": ts,
    "day_of_week": ts.day_name(),
    "hour": hour,
    "distance_km": distance_km,
    "duration_min": duration_min,
    "fare": fare,
    "payment_method": payment,
    "weather": weather_row,
})

print(f"Escribiendo {OUTPUT_FILE}...")
df.to_csv(OUTPUT_FILE, index=False)
print("Listo.")
print(f"  Registros: {len(df):,}")
print(f"  Tarjetas unicas: {df['card_id'].nunique():,}")
print(f"  Recaudacion total simulada: {df['fare'].sum():,.2f} PAB")
print(f"  Duracion promedio: {df['duration_min'].mean():.1f} min")
print(f"  Distribucion por modo:\n{df['transport_mode'].value_counts()}")
