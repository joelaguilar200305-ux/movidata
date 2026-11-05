

from repositories.mongo_viajes_repository import MongoViajesRepository


def main():
    repositorio = None

    try:
        repositorio = MongoViajesRepository()

        print("=== CONSULTAS AVANZADAS MOVIDATA ===")

        # 1. FILTRO POR DISTRITO
        print("\n1. Viajes en San Miguelito")

        viajes = repositorio.buscar_por_filtro(
            {"district": "San Miguelito"},
            limite=5
        )

        for viaje in viajes:
            print(
                viaje.trip_id,
                viaje.transport_mode
            )

        # 2. FILTRO POR TRANSPORTE
        print("\n2. Total de viajes en Metrobus")

        total = repositorio.contar_documentos(
            {"transport_mode": "Metrobus"}
        )

        print("Total Metrobus:", total)

        # 3. FILTRO POR RUTA
        print("\n3. Viajes de la ruta Tumba Muerto")

        viajes_ruta = repositorio.buscar_por_filtro(
            {"route_line": "Tumba Muerto"},
            limite=5
        )

        for viaje in viajes_ruta:
            print(
                viaje.trip_id,
                viaje.route_line
            )

        # 4. AGREGACION POR DISTRITO
        print("\n4. Top 5 distritos con mas viajes")

        pipeline_distritos = [
            {
                "$group": {
                    "_id": "$district",
                    "total": {"$sum": 1}
                }
            },
            {"$sort": {"total": -1}},
            {"$limit": 5}
        ]

        resultados = repositorio.agregar(
            pipeline_distritos
        )

        for resultado in resultados:
            print(resultado)

        # 5. AGREGACION POR HORA
        print("\n5. Distribucion de viajes por hora")

        pipeline_horas = [
            {
                "$group": {
                    "_id": {
                        "$toInt": "$hour"
                    },
                    "total": {
                        "$sum": 1
                    }
                }
            },
            {
                "$sort": {
                    "_id": 1
                }
            }
        ]

        resultados = repositorio.agregar(
            pipeline_horas
        )

        for resultado in resultados:
            print(resultado)

        print("\nCONSULTAS FINALIZADAS")

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
