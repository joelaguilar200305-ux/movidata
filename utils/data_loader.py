import pandas as pd

from exceptions.data_load_error import DataLoadError


class DataLoader:
    """Lee, valida y limpia el CSV de viajes."""

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
        try:
            data = pd.read_csv(self._file_path)
        except FileNotFoundError as error:
            raise DataLoadError(
                f"No se encontró el archivo: {self._file_path}"
            ) from error
        except (pd.errors.ParserError, UnicodeDecodeError, OSError) as error:
            raise DataLoadError(
                f"Error al leer el archivo CSV: {error}"
            ) from error

        if data.empty:
            raise DataLoadError("El archivo CSV está vacío.")

        missing = [column for column in self.COLUMNS
                   if column not in data.columns]

        if missing:
            raise DataLoadError(
                f"Faltan columnas obligatorias: {missing}"
            )

        initial_records = len(data)

        # Limpiar espacios de las columnas de texto
        for column in self.TEXT_COLUMNS:
            data[column] = data[column].astype("string").str.strip()

        # Convertir fechas y valores numéricos
        data["boarding_datetime"] = pd.to_datetime(
            data["boarding_datetime"],
            errors="coerce"
        )

        for column in self.NUMERIC_COLUMNS:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

        # Eliminar registros con valores vacíos o inválidos
        data = data.dropna(subset=self.COLUMNS)

        # Eliminar viajes duplicados
        data = data.drop_duplicates(subset="trip_id")

        # Validar hora
        data = data[data["hour"].between(0, 23)]

        # Validar tipo de transporte
        data = data[data["transport_mode"].isin(self.TRANSPORT_MODES)]

        # Validar tipo de usuario
        data = data[data["user_type"].isin(self.USER_TYPES)]

        # Validar valores numéricos negativos
        data = data[
            (data["distance_km"] >= 0)
            & (data["duration_min"] >= 0)
            & (data["fare"] >= 0)
        ]

        # Convertir hora a entero
        data["hour"] = data["hour"].astype(int)

        loaded_records = len(data)
        discarded_records = initial_records - loaded_records

        # Verificar integridad de los registros
        if data["trip_id"].duplicated().any():
            raise DataLoadError(
                "Se encontraron trip_id duplicados después de la limpieza."
            )

        print(f"Registros iniciales: {initial_records:,}")
        print(f"Registros cargados: {loaded_records:,}")
        print(f"Registros descartados: {discarded_records:,}")

        return data