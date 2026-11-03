
import os
import csv
import argparse
from itertools import islice
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient, UpdateOne
from pymongo.errors import PyMongoError

# CONFIGURACION
BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env")

URI = os.getenv("MONGODB_URI")
ARCHIVO = BASE / "data" / "viajes_movidata.csv"

TAMANO_BLOQUE = 1000

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inicio", type=int, default=0)
    args = parser.parse_args()

    if args.inicio < 0:
        print("ERROR: El inicio no puede ser negativo")
        return

    if not URI:
        print("ERROR: Falta MONGODB_URI en .env")
        return

    if not ARCHIVO.exists():
        print("ERROR: No existe el archivo CSV")
        return

    cliente = None

    try:
        cliente = MongoClient(
            URI,
            serverSelectionTimeoutMS=5000
        )

        cliente.admin.command("ping")

        db = cliente["movidata"]
        coleccion = db["viajes"]

        print("Conexion exitosa con MongoDB Atlas")

        total_antes = coleccion.count_documents({})
        print("Documentos existentes:", total_antes)

        # Indice unico para evitar duplicados
        coleccion.create_index("trip_id", unique=True)

        with open(
            ARCHIVO,
            encoding="utf-8-sig",
            newline=""
        ) as archivo:

            lector = csv.DictReader(archivo)

            if "trip_id" not in (lector.fieldnames or []):
                raise ValueError("Falta la columna trip_id")

            # Saltar los registros anteriores
            registros = list(
                islice(lector, args.inicio, args.inicio + TAMANO_BLOQUE)
            )

        if not registros:
            print("No hay registros en este rango")
            return

        operaciones = []

        for fila in registros:
            identificador = fila["trip_id"]

            if not identificador:
                raise ValueError("trip_id vacio")

            operaciones.append(
                UpdateOne(
                    {"trip_id": identificador},
                    {"$setOnInsert": fila},
                    upsert=True
                )
            )

        resultado = coleccion.bulk_write(
            operaciones,
            ordered=False
        )

        print("\nCARGA FINALIZADA")
        print("Inicio del bloque:", args.inicio)
        print("Registros procesados:", len(registros))
        print("Nuevos insertados:", resultado.upserted_count)
        print("Ya existentes:", resultado.matched_count)
        print(
            "Total en MongoDB:",
            coleccion.count_documents({})
        )

    except (PyMongoError, OSError, ValueError) as error:
        print("ERROR:", type(error).__name__, str(error))

    finally:
        if cliente is not None:
            cliente.close()


if __name__ == "__main__":
    main()
