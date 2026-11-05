
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

    with MongoClient(
        uri,
        serverSelectionTimeoutMS=5000
    ) as cliente:

        cliente.admin.command("ping")
        db = cliente["movidata"]

        consultas = [
            ("Distrito San Miguelito",
             {"district": "San Miguelito"}),
            ("Transporte Metrobus",
             {"transport_mode": "Metrobus"})
        ]

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

            etapas = resultado.get("stages", [])

            for etapa in etapas:
                cursor = etapa.get("$cursor", {})
                estadisticas = cursor.get(
                    "executionStats", {}
                )

                if estadisticas:
                    print(
                        "Documentos examinados:",
                        estadisticas.get(
                            "totalDocsExamined"
                        )
                    )
                    print(
                        "Claves examinadas:",
                        estadisticas.get(
                            "totalKeysExamined"
                        )
                    )
                    print(
                        "Tiempo (ms):",
                        estadisticas.get(
                            "executionTimeMillis"
                        )
                    )

            print("Analisis completado")

        print("\nPRUEBAS FINALIZADAS")


if __name__ == "__main__":
    main()
