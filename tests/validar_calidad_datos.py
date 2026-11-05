
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
        coleccion = cliente["movidata"]["viajes"]

        print("=== CALIDAD DE DATOS MOVIDATA ===")

        total = coleccion.count_documents({})
        print("Total documentos:", total)

        print("\n1. VALIDACION DE INDICE UNICO")

        indices = list(coleccion.list_indexes())
        indice_unico = any(
            indice.get("key", {}).get("trip_id") == 1
            and indice.get("unique", False)
            for indice in indices
        )

        print("trip_id unico:", indice_unico)

        print("\n2. VALIDACION DE TIPOS")

        campos = [
            "trip_id",
            "boarding_datetime",
            "transport_mode",
            "district",
            "route_line",
            "hour"
        ]

        for campo in campos:
            incorrectos = coleccion.count_documents({
                campo: {
                    "$not": {
                        "$type": "string"
                    }
                }
            })

            print(
                campo,
                "tipos diferentes de string:",
                incorrectos
            )

        print("\n3. VALIDACION DE HORAS")

        pipeline_horas = [
            {
                "$match": {
                    "hour": {
                        "$not": {
                            "$regex": r"^(?:[01]?\d|2[0-3])$"
                        }
                    }
                }
            },
            {"$count": "invalidas"}
        ]

        resultado = list(
            coleccion.aggregate(pipeline_horas)
        )

        invalidas = (
            resultado[0]["invalidas"]
            if resultado else 0
        )

        print("Horas invalidas:", invalidas)

        print("\n4. VALIDACION DE FECHAS")

        pipeline_fechas = [
            {
                "$match": {
                    "boarding_datetime": {
                        "$not": {
                            "$regex":
                            r"^\d{4}-\d{2}-\d{2} "
                            r"\d{2}:\d{2}:\d{2}$"
                        }
                    }
                }
            },
            {"$count": "invalidas"}
        ]

        resultado = list(
            coleccion.aggregate(pipeline_fechas)
        )

        invalidas = (
            resultado[0]["invalidas"]
            if resultado else 0
        )

        print("Fechas con formato invalido:", invalidas)

        print("\nVALIDACION FINALIZADA")


if __name__ == "__main__":
    main()
