
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

BASE = Path(__file__).resolve().parent.parent
load_dotenv(BASE / ".env")


def main():
    uri = os.getenv("MONGODB_URI")

    if not uri:
        raise ValueError("Falta MONGODB_URI en .env")

    consultas = [
        ("Distrito San Miguelito",
         {"district": "San Miguelito"}),
        ("Transporte Metrobus",
         {"transport_mode": "Metrobus"})
    ]

    with MongoClient(
        uri,
        serverSelectionTimeoutMS=5000
    ) as cliente:

        cliente.admin.command("ping")
        db = cliente["movidata"]

        print("=== RENDIMIENTO DE CONTEOS ===")

        for nombre, filtro in consultas:
            pipeline = [
                {"$match": filtro},
                {"$count": "total"}
            ]

            resultado = db.command(
                "explain",
                {
                    "aggregate": "viajes",
                    "pipeline": pipeline,
                    "cursor": {},
                    "maxTimeMS": 15000
                },
                verbosity="executionStats"
            )

            print(f"\nConsulta: {nombre}")

            estadisticas = resultado.get(
                "executionStats"
            )

            if not estadisticas:
                for etapa in resultado.get("stages", []):
                    cursor = etapa.get("$cursor", {})
                    estadisticas = cursor.get(
                        "executionStats"
                    )
                    if estadisticas:
                        break

            if estadisticas:
                print(
                    "Documentos examinados:",
                    estadisticas.get("totalDocsExamined")
                )
                print(
                    "Claves examinadas:",
                    estadisticas.get("totalKeysExamined")
                )
                print(
                    "Tiempo (ms):",
                    estadisticas.get("executionTimeMillis")
                )
            else:
                print(
                    "Estadisticas no encontradas "
                    "en el formato esperado"
                )

        print("\nPRUEBAS FINALIZADAS")


if __name__ == "__main__":
    main()
