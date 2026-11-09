import sys
import unittest
import tempfile
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))

from utils.data_loader import DataLoader
from exceptions.data_load_error import DataLoadError


class TestDataLoader(unittest.TestCase):

    def test_carga_csv_correctamente(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "viajes.csv"

            datos = {
                "trip_id": ["T001", "T001", "T002"],
                "card_id": ["C001", "C001", "C002"],
                "user_type": ["Regular", "Regular", "Regular"],
                "district": ["San Miguelito"] * 3,
                "transport_mode": ["Metro"] * 3,
                "route_line": ["L1"] * 3,
                "origin": ["Albrook"] * 3,
                "destination": ["San Miguelito"] * 3,
                "boarding_datetime": [
                    "2026-01-01 08:00:00",
                    "2026-01-01 08:00:00",
                    "2026-01-01 09:00:00"
                ],
                "day_of_week": ["Jueves"] * 3,
                "hour": [8, 8, 25],
                "distance_km": [10, 10, 5],
                "duration_min": [20, 20, 15],
                "fare": [0.35, 0.35, 0.25],
                "payment_method": ["Tarjeta"] * 3,
                "weather": ["Soleado"] * 3,
            }

            pd.DataFrame(datos).to_csv(
                ruta,
                index=False
            )

            loader = DataLoader(str(ruta))
            resultado = loader.load_csv()

            self.assertEqual(len(resultado), 1)
            self.assertEqual(
                resultado.iloc[0]["trip_id"],
                "T001"
            )

    def test_archivo_inexistente(self):
        loader = DataLoader("archivo_inexistente.csv")

        with self.assertRaises(DataLoadError):
            loader.load_csv()

    def test_columnas_faltantes(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "incompleto.csv"

            pd.DataFrame({
                "trip_id": ["T001"]
            }).to_csv(ruta, index=False)

            loader = DataLoader(str(ruta))

            with self.assertRaises(DataLoadError):
                loader.load_csv()


if __name__ == "__main__":
    unittest.main()