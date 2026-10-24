import pandas as pd


class DataLoader:
    """Lee y limpia el CSV de viajes. No guarda en MongoDB."""

    # Las 16 columnas del diccionario de datos
    COLUMNS = [
        "trip_id", "card_id", "user_type", "district", "transport_mode",
        "route_line", "origin", "destination", "boarding_datetime",
        "day_of_week", "hour", "distance_km", "duration_min", "fare",
        "payment_method", "weather",
    ]
    TEXT_COLUMNS = [
        "trip_id", "card_id", "user_type", "district", "transport_mode",
        "route_line", "origin", "destination", "day_of_week",
        "payment_method", "weather",
    ]
    NUMERIC_COLUMNS = ["hour", "distance_km", "duration_min", "fare"]
    TRANSPORT_MODES = ["Metro", "Metrobus"]
    USER_TYPES = ["Regular", "Estudiante", "Jubilado", "Turista"]

    def __init__(self, file_path: str = "data/viajes_movidata.csv") -> None:
        self._file_path = file_path

    def load_csv(self) -> pd.DataFrame:
        # 1. Leer el CSV con pandas
        try:
            data = pd.read_csv(self._file_path)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"No se encontró el archivo {self._file_path}. "
                "Genera el dataset con scripts/generar_dataset_movidata.py"
            )

        # 2. Verificar que estén las 16 columnas
        missing = [c for c in self.COLUMNS if c not in data.columns]
        if missing:
            raise ValueError(f"Faltan columnas en el CSV: {missing}")

        initial_records = len(data)

        # 3. Corregir: quitar espacios sobrantes en los textos
        for column in self.TEXT_COLUMNS:
            data[column] = data[column].str.strip()

        # 4. Verificar tipos: lo que no se pueda convertir queda vacío (NaN)
        data["boarding_datetime"] = pd.to_datetime(data["boarding_datetime"], errors="coerce")
        for column in self.NUMERIC_COLUMNS:
            data[column] = pd.to_numeric(data[column], errors="coerce")

        # 5. Descartar valores inválidos
        data = data.dropna()
        data = data.drop_duplicates(subset="trip_id")
        data = data[data["hour"].between(0, 23)]
        data = data[data["transport_mode"].isin(self.TRANSPORT_MODES)]
        data = data[data["user_type"].isin(self.USER_TYPES)]
        data = data[
            (data["distance_km"] >= 0)
            & (data["duration_min"] >= 0)
            & (data["fare"] >= 0)
        ]
        data = data.assign(hour=data["hour"].astype(int))

        # 6. Reportar cuántos registros se cargaron
        loaded_records = len(data)
        print(f"Registros iniciales: {initial_records:,}")
        print(f"Registros cargados: {loaded_records:,}")
        print(f"Registros descartados: {initial_records - loaded_records:,}")

        return data