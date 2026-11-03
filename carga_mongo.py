
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
    parser.add_argument("--cantidad", type=int, default=1000)
    args = parser.parse_args()

    if args.inicio < 0:
        print("ERROR: El inicio no puede ser negativo")
        return

    if args.cantidad < 1 or args.cantidad > 10000:
        print("ERROR: cantidad debe estar entre 1 y 10000")
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

        coleccion = cliente["movidata"]["viajes"]

        print("Conexion exitosa con MongoDB Atlas")
        print("Documentos iniciales:",
              coleccion.count_documents({}))

        # Evitar duplicados
        coleccion.create_index("trip_id", unique=True)

        procesados = 0
        insertados = 0
        existentes = 0

        with open(
            ARCHIVO,
            encoding="utf-8-sig",
            newline=""
        ) as archivo:

            lector = csv.DictReader(archivo)

            if "trip_id" not in (lector.fieldnames or []):
                raise ValueError("Falta la columna trip_id")

            filas = islice(
                lector,
                args.inicio,
                args.inicio + args.cantidad
            )

            while True:
                bloque = list(islice(filas, TAMANO_BLOQUE))

                if not bloque:
                    break

                operaciones = []

                for fila in bloque:
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

                procesados += len(bloque)
                insertados += resultado.upserted_count
                existentes += resultado.matched_count

                print(
                    "Procesados:", procesados,
                    "| Nuevos:", insertados,
                    "| Existentes:", existentes
                )

        print("\nCARGA FINALIZADA")
        print("Inicio:", args.inicio)
        print("Registros procesados:", procesados)
        print("Nuevos insertados:", insertados)
        print("Ya existentes:", existentes)
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
