
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

BASE = Path(__file__).resolve().parent.parent
load_dotenv(BASE / ".env")

CAMPOS = [
    "trip_id",
    "boarding_datetime",
    "transport_mode",
    "district",
    "route_line",
    "hour"
]


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

        print("=== VALIDACION MOVIDATA ===")

        total = coleccion.count_documents({})
        print("Total documentos:", total)

        print("\n1. CAMPOS FALTANTES O VACIOS")

        for campo in CAMPOS:
            cantidad = coleccion.count_documents({
                "$or": [
                    {campo: {"$exists": False}},
                    {campo: None},
                    {campo: ""}
                ]
            })

            print(f"{campo}: {cantidad}")

        print("\n2. TIPOS DE DATOS")

        documento = coleccion.find_one(
            {},
            {"_id": 0}
        )

        if documento:
            for campo in CAMPOS:
                valor = documento.get(campo)
                print(
                    campo,
                    type(valor).__name__,
                    repr(valor)
                )

        print("\n3. DOCUMENTOS DE EJEMPLO")

        for documento in coleccion.find(
            {},
            {"_id": 0, "trip_id": 1,
             "district": 1, "transport_mode": 1}
        ).limit(3):
            print(documento)

        print("\nVALIDACION FINALIZADA")


if __name__ == "__main__":
    main()
