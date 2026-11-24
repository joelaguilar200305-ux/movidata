
import os
from dotenv import load_dotenv
from pymongo import MongoClient


def main():
    load_dotenv(".env")
    cliente = MongoClient(os.environ["MONGODB_URI"])

    try:
        coleccion = cliente["movidata"]["viajes"]

        consultas = {
            "Busqueda por trip_id": {
                "trip_id": "VJE000000001"
            },
            "Busqueda por distrito": {
                "district": "San Miguelito"
            },
            "Busqueda por transporte": {
                "transport_mode": "Metrobus"
            }
        }

        print("=== COMPARACION DE INDICES MOVIDATA ===")

        for nombre, filtro in consultas.items():
            plan = coleccion.find(filtro).limit(5).explain()

            estadisticas = plan["executionStats"]

            print("\nConsulta:", nombre)
            print(
                "Documentos examinados:",
                estadisticas["totalDocsExamined"]
            )
            print(
                "Claves examinadas:",
                estadisticas["totalKeysExamined"]
            )
            print(
                "Tiempo (ms):",
                estadisticas["executionTimeMillis"]
            )

        print("\nCOMPARACION FINALIZADA")

    finally:
        cliente.close()


if __name__ == "__main__":
    main()
