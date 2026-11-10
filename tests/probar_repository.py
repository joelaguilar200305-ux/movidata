
from repositories.mongo_viaje_repository import 	MongoViajeRepository


def main():
    repositorio = None

    try:
        repositorio = 	MongoViajeRepository()

        print("=== PRUEBAS REPOSITORY MOVIDATA ===")

        print("\n1. Consultar 5 viajes")
        viajes = repositorio.buscar_por_filtro({}, limite=5)

        for viaje in viajes:
            print(
                viaje.trip_id,
                viaje.transport_mode,
                viaje.district
            )

        print("\n2. Contar viajes de Metrobus")
        total = repositorio.contar_documentos(
            {"transport_mode": "Metrobus"}
        )
        print("Total Metrobus:", total)

        print("\n3. Agrupar viajes por transporte")
        resultados = repositorio.agregar([
            {
                "$group": {
                    "_id": "$transport_mode",
                    "total": {"$sum": 1}
                }
            },
            {
                "$sort": {"total": -1}
            }
        ])

        for resultado in resultados:
            print(resultado)

        print("\nPRUEBAS FINALIZADAS")

    except Exception as error:
        print(
            "ERROR:",
            type(error).__name__,
            str(error)
        )
        raise

    finally:
        if repositorio is not None:
            repositorio.cerrar()


if __name__ == "__main__":
    main()
